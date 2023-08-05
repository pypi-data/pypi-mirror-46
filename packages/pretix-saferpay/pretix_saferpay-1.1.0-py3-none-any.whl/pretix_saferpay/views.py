import hashlib
import json
import logging
import requests
import uuid
from django.contrib import messages
from django.core import signing
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from pretix.base.models import Order, OrderPayment, Quota
from pretix.base.payment import PaymentException
from pretix.base.services.locking import LockTimeoutException
from pretix.multidomain.urlreverse import eventreverse

logger = logging.getLogger(__name__)


@xframe_options_exempt
def redirect_view(request, *args, **kwargs):
    signer = signing.Signer(salt='safe-redirect')
    try:
        url = signer.unsign(request.GET.get('url', ''))
    except signing.BadSignature:
        return HttpResponseBadRequest('Invalid parameter')

    r = render(request, 'pretix_saferpay/redirect.html', {
        'url': url,
    })
    r._csp_ignore = True
    return r


def handle_transaction_result(payment):
    pprov = payment.payment_provider
    trans = payment.info_data

    if trans.get('Status') == 'AUTHORIZED' and payment.state not in (OrderPayment.PAYMENT_STATE_CONFIRMED,
                                                                     OrderPayment.PAYMENT_STATE_REFUNDED):
        payment.order.log_action('pretix_saferpay.event.authorized')
        req = pprov._post('Payment/v1/Transaction/Capture', json={
            "RequestHeader": {
                "SpecVersion": "1.10",
                "CustomerId": pprov.settings.customer_id,
                "RequestId": str(uuid.uuid4()),
                "RetryIndicator": 0
            },
            "TransactionReference": {
                "TransactionId": payment.info_data.get('Id')
            }
        })
        req.raise_for_status()
        data = req.json()
        if data['Status'] == 'CAPTURED':
            payment.order.log_action('pretix_saferpay.event.captured')
            trans['Status'] = 'CAPTURED'
            trans['CaptureId'] = data['CaptureId']
            payment.info = json.dumps(trans)
            payment.save(update_fields=['info'])
            payment.confirm()

    elif trans.get('Status') == 'CAPTURED' and payment.state not in (OrderPayment.PAYMENT_STATE_CONFIRMED,
                                                                     OrderPayment.PAYMENT_STATE_REFUNDED):
        payment.order.log_action('pretix_saferpay.event.captured')
        payment.confirm()
    elif trans.get('Status') == 'PENDING' and payment.state == OrderPayment.PAYMENT_STATE_CREATED:
        payment.state = OrderPayment.PAYMENT_STATE_PENDING
        payment.save(update_fields=['state'])


def capture(payment: OrderPayment):
    if payment.state == OrderPayment.PAYMENT_STATE_CONFIRMED:
        return

    pprov = payment.payment_provider
    try:
        if payment.info_data.get('Status') == 'CAPTURED':
            return

        if 'Token' in payment.info_data:
            req = pprov._post('Payment/v1/PaymentPage/Assert', json={
                "RequestHeader": {
                    "SpecVersion": "1.10",
                    "CustomerId": pprov.settings.customer_id,
                    "RequestId": str(uuid.uuid4()),
                    "RetryIndicator": 0
                },
                "Token": payment.info_data.get('Token')
            })
            req.raise_for_status()
            data = req.json()
            trans = data['Transaction']
            if 'PaymentMeans' in data:
                trans['PaymentMeans'] = data['PaymentMeans']

            payment.info = json.dumps(trans)
            payment.save(update_fields=['info'])
            handle_transaction_result(payment)
        elif payment.info_data.get('Status') == 'AUTHORIZED':
            handle_transaction_result(payment)
        else:
            raise PaymentException('Unknown payment state')

    except requests.exceptions.HTTPError as e:
        payment.order.log_action('pretix.event.order.payment.failed', {
            'local_id': payment.local_id,
            'provider': payment.provider,
            'data': e.response.text
        })
        raise PaymentException(_('We had trouble communicating with Saferpay. Please try again and get in touch '
                                 'with us if this problem persists.'))


class SaferpayOrderView:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.order = request.event.orders.get(code=kwargs['order'])
            if hashlib.sha1(self.order.secret.lower().encode()).hexdigest() != kwargs['hash'].lower():
                raise Http404('')
        except Order.DoesNotExist:
            # Do a hash comparison as well to harden timing attacks
            if 'abcdefghijklmnopq'.lower() == hashlib.sha1('abcdefghijklmnopq'.encode()).hexdigest():
                raise Http404('')
            else:
                raise Http404('')
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def payment(self):
        return get_object_or_404(self.order.payments,
                                 pk=self.kwargs['payment'],
                                 provider__startswith='saferpay')

    @cached_property
    def pprov(self):
        return self.payment.payment_provider


@method_decorator(xframe_options_exempt, 'dispatch')
class ReturnView(SaferpayOrderView, View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('action') == 'success':
            if self.payment.state not in (OrderPayment.PAYMENT_STATE_CONFIRMED, OrderPayment.PAYMENT_STATE_REFUNDED,
                                          OrderPayment.PAYMENT_STATE_CANCELED):
                try:
                    capture(self.payment)
                except PaymentException as e:
                    messages.error(self.request, str(e))
                except LockTimeoutException:
                    messages.error(self.request, _('We received your payment but were unable to mark your ticket as '
                                                   'the server was too busy. Please check beck in a couple of '
                                                   'minutes.'))
                except Quota.QuotaExceededException:
                    messages.error(self.request, _('We received your payment but were unable to mark your ticket as '
                                                   'paid as one of your ordered products is sold out. Please contact '
                                                   'the event organizer for further steps.'))
        elif kwargs.get('action') == 'fail':
            self.order.log_action('pretix.event.order.payment.failed', {
                'local_id': self.payment.local_id,
                'provider': self.payment.provider,
            })
            self.payment.state = OrderPayment.PAYMENT_STATE_FAILED
            self.payment.save(update_fields=['state'])
        elif kwargs.get('action') == 'abort':
            self.order.log_action('pretix.event.order.payment.canceled', {
                'local_id': self.payment.local_id,
                'provider': self.payment.provider,
            })
            self.payment.state = OrderPayment.PAYMENT_STATE_CANCELED
            self.payment.save(update_fields=['state'])

        return self._redirect_to_order()

    def _redirect_to_order(self):
        self.order.refresh_from_db()
        if self.request.session.get('payment_saferpay_order_secret') != self.order.secret:
            messages.error(self.request, _('Sorry, there was an error in the payment process. Please check the link '
                                           'in your emails to continue.'))
            return redirect(eventreverse(self.request.event, 'presale:event.index'))

        return redirect(eventreverse(self.request.event, 'presale:event.order', kwargs={
            'order': self.order.code,
            'secret': self.order.secret
        }) + ('?paid=yes' if self.order.status == Order.STATUS_PAID else ''))


@method_decorator(csrf_exempt, 'dispatch')
class WebhookView(View):
    def get(self, request, *args, **kwargs):
        from .tasks import capture_task

        capture_task.apply_async(args=(self.payment.pk,), countdown=30)
        return HttpResponse(status=200)

    @cached_property
    def payment(self):
        return get_object_or_404(OrderPayment.objects.filter(order__event=self.request.event),
                                 pk=self.kwargs['payment'],
                                 provider__startswith='saferpay')
