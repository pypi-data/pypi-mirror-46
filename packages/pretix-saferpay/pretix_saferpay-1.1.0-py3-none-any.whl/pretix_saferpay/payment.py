from collections import OrderedDict

import hashlib
import json
import logging
import requests
import urllib.parse
import uuid
from django import forms
from django.conf import settings
from django.core import signing
from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.translation import pgettext, ugettext_lazy as _
from requests import HTTPError

from pretix.base.decimal import round_decimal
from pretix.base.models import Event, OrderPayment, OrderRefund
from pretix.base.payment import BasePaymentProvider, PaymentException
from pretix.base.settings import SettingsSandbox
from pretix.multidomain.urlreverse import build_absolute_uri

logger = logging.getLogger(__name__)


class SaferpaySettingsHolder(BasePaymentProvider):
    identifier = 'saferpay'
    verbose_name = _('Saferpay')
    is_enabled = False
    is_meta = True

    def __init__(self, event: Event):
        super().__init__(event)
        self.settings = SettingsSandbox('payment', 'saferpay', event)

    @property
    def settings_form_fields(self):
        fields = [
            ('endpoint',
             forms.ChoiceField(
                 label=_('Endpoint'),
                 initial='live',
                 choices=(
                     ('live', pgettext('saferpay', 'Live')),
                     ('test', pgettext('saferpay', 'Testing')),
                 ),
             )),
            ('api_user',
             forms.CharField(
                 label=_('API Username'),
             )),
            ('api_pass',
             forms.CharField(
                 label=_('API Password'),
             )),
            ('customer_id',
             forms.CharField(
                 label=_('Customer ID'),
             )),
            ('terminal_id',
             forms.CharField(
                 label=_('Terminal ID'),
             )),
        ]
        d = OrderedDict(
            fields + [
                ('method_visa',
                 forms.BooleanField(
                     label=_('VISA'),
                     required=False,
                 )),
                ('method_mastercard',
                 forms.BooleanField(
                     label=_('MasterCard'),
                     required=False,
                 )),
                ('method_diners',
                 forms.BooleanField(
                     label=_('Diners'),
                     required=False,
                 )),
                ('method_jcb',
                 forms.BooleanField(
                     label=_('JCB'),
                     required=False,
                 )),
                ('method_amex',
                 forms.BooleanField(
                     label=_('American Express'),
                     required=False,
                 )),
                ('method_bancontact',
                 forms.BooleanField(
                     label=_('Bancontact'),
                     required=False,
                 )),
                ('method_eprzelewy',
                 forms.BooleanField(
                     label=_('ePrzelewy'),
                     required=False,
                 )),
                ('method_eps',
                 forms.BooleanField(
                     label=_('eps'),
                     required=False,
                 )),
                ('method_giropay',
                 forms.BooleanField(
                     label=_('giropay'),
                     required=False,
                 )),
                ('method_ideal',
                 forms.BooleanField(
                     label=_('iDEAL'),
                     required=False,
                 )),
                # Disabled because we couldn't test the flow which is documented as being different than the others
                # (i.e. it has a payment state and uses callbacks)
                #('method_paydirekt',
                # forms.BooleanField(
                #     label=_('paydirekt'),
                #     required=False,
                # )),
                ('method_paypal',
                 forms.BooleanField(
                     label=_('PayPal'),
                     required=False,
                 )),
                ('method_postfinance_card',
                 forms.BooleanField(
                     label=_('PostFinance Card'),
                     required=False,
                 )),
                ('method_postfinance_efinance',
                 forms.BooleanField(
                     label=_('PostFinance eFinance'),
                     required=False,
                 )),
                ('method_sepadebit',
                 forms.BooleanField(
                     label=_('SEPA Direct Debit'),
                     required=False,
                 )),
                ('method_sofort',
                 forms.BooleanField(
                     label=_('Sofort'),
                     required=False,
                 )),
            ] + list(super().settings_form_fields.items())
        )
        d.move_to_end('_enabled', last=False)
        return d


class SaferpayMethod(BasePaymentProvider):
    method = ''
    abort_pending_allowed = False
    refunds_allowed = True
    cancel_flow = True
    payment_methods = []

    def __init__(self, event: Event):
        super().__init__(event)
        self.settings = SettingsSandbox('payment', 'saferpay', event)

    @property
    def settings_form_fields(self):
        return {}

    @property
    def identifier(self):
        return 'saferpay_{}'.format(self.method)

    @property
    def is_enabled(self) -> bool:
        return self.settings.get('_enabled', as_type=bool) and self.settings.get('method_{}'.format(self.method),
                                                                                 as_type=bool)

    def payment_refund_supported(self, payment: OrderPayment) -> bool:
        return self.refunds_allowed

    def payment_partial_refund_supported(self, payment: OrderPayment) -> bool:
        return self.refunds_allowed

    def payment_prepare(self, request, payment):
        return self.checkout_prepare(request, None)

    def payment_is_valid_session(self, request: HttpRequest):
        return True

    def payment_form_render(self, request) -> str:
        template = get_template('pretix_saferpay/checkout_payment_form.html')
        ctx = {'request': request, 'event': self.event, 'settings': self.settings}
        return template.render(ctx)

    def checkout_confirm_render(self, request) -> str:
        template = get_template('pretix_saferpay/checkout_payment_confirm.html')
        ctx = {'request': request, 'event': self.event, 'settings': self.settings, 'provider': self}
        return template.render(ctx)

    def payment_can_retry(self, payment):
        return self._is_still_available(order=payment.order)

    def payment_pending_render(self, request, payment) -> str:
        if payment.info:
            payment_info = json.loads(payment.info)
        else:
            payment_info = None
        template = get_template('pretix_saferpay/pending.html')
        ctx = {
            'request': request,
            'event': self.event,
            'settings': self.settings,
            'provider': self,
            'order': payment.order,
            'payment': payment,
            'payment_info': payment_info,
        }
        return template.render(ctx)

    def payment_control_render(self, request, payment) -> str:
        if payment.info:
            payment_info = json.loads(payment.info)
            if 'amount' in payment_info:
                payment_info['amount'] /= 10 ** settings.CURRENCY_PLACES.get(self.event.currency, 2)
        else:
            payment_info = None
        template = get_template('pretix_saferpay/control.html')
        ctx = {
            'request': request,
            'event': self.event,
            'settings': self.settings,
            'payment_info': payment_info,
            'payment': payment,
            'method': self.method,
            'provider': self,
        }
        return template.render(ctx)

    def execute_refund(self, refund: OrderRefund):
        d = refund.payment.info_data

        try:
            if self.cancel_flow and refund.amount == refund.payment.amount:
                if 'Id' not in d:
                    raise PaymentException(_('The payment has not been captured successfully and can therefore not be '
                                             'refunded.'))

                req = self._post('Payment/v1/Transaction/Cancel', json={
                    "RequestHeader": {
                        "SpecVersion": "1.10",
                        "CustomerId": self.settings.customer_id,
                        "RequestId": str(uuid.uuid4()),
                        "RetryIndicator": 0
                    },
                    "TransactionReference": {
                        "TransactionId": d.get('Id')
                    }
                })
                if req.status_code == 200:
                    refund.info = req.text
                    refund.save(update_fields=['info'])
                    refund.done()

                try:
                    err = req.json()
                except:
                    req.raise_for_status()
                else:
                    if err['ErrorName'] not in ('ACTION_NOT_SUPPORTED', 'TRANSACTION_ALREADY_CAPTURED', 'TRANSACTION_IN_WRONG_STATE'):
                        req.raise_for_status()

            if 'CaptureId' not in d:
                raise PaymentException(_('The payment has not been captured successfully and can therefore not be '
                                         'refunded.'))

            req = self._post('Payment/v1/Transaction/Refund', json={
                "RequestHeader": {
                    "SpecVersion": "1.10",
                    "CustomerId": self.settings.customer_id,
                    "RequestId": str(uuid.uuid4()),
                    "RetryIndicator": 0
                },
                "Refund": {
                    "Amount": {
                        "Value": str(self._decimal_to_int(refund.amount)),
                        "CurrencyCode": self.event.currency
                    },
                    "OrderId": "{}-{}-R-{}".format(self.event.slug.upper(), refund.order.code, refund.local_id),
                    "Description": "Order {}-{}".format(self.event.slug.upper(), refund.order.code),
                },
                "CaptureReference": {
                    "CaptureId": d.get('CaptureId')
                }
            })
            req.raise_for_status()
            refund.info_data = req.json()
            refund.save(update_fields=['info'])

            if refund.info_data['Transaction'].get('Status') == 'AUTHORIZED':
                req = self._post('Payment/v1/Transaction/Capture', json={
                    "RequestHeader": {
                        "SpecVersion": "1.10",
                        "CustomerId": self.settings.customer_id,
                        "RequestId": str(uuid.uuid4()),
                        "RetryIndicator": 0
                    },
                    "TransactionReference": {
                        "TransactionId": refund.info_data['Transaction'].get('Id')
                    }
                })
                req.raise_for_status()
                data = req.json()
                if data['Status'] == 'CAPTURED':
                    refund.order.log_action('pretix_saferpay.event.paid')
                    trans = refund.info_data
                    trans['Transaction']['Status'] = 'CAPTURED'
                    trans['Transaction']['CaptureId'] = data['CaptureId']
                    refund.info = json.dumps(trans)
                    refund.save(update_fields=['info'])
                    refund.done()

        except HTTPError:
            logger.exception('Saferpay error: %s' % req.text)
            try:
                refund.info_data = req.json()
            except:
                refund.info_data = {
                    'error': True,
                    'detail': req.text
                }
            refund.state = OrderRefund.REFUND_STATE_FAILED
            refund.save()
            refund.order.log_action('pretix.event.order.refund.failed', {
                'local_id': refund.local_id,
                'provider': refund.provider,
                'data': refund.info_data
            })
            raise PaymentException(_('We had trouble communicating with Saferpay. Please try again and get in touch '
                                     'with us if this problem persists.'))

    @property
    def test_mode_message(self):
        if self.settings.endpoint == 'test':
            return _('The Saferpay plugin is operating in test mode. No money will actually be transferred.')
        return None

    def _post(self, endpoint, *args, **kwargs):
        r = requests.post(
            'https://{env}.saferpay.com/api/{ep}'.format(
                env='www' if self.settings.get('endpoint') == 'live' else 'test',
                ep=endpoint,
            ),
            auth=(self.settings.get('api_user'), self.settings.get('api_pass')),
            *args, **kwargs
        )
        return r

    def _get(self, endpoint, *args, **kwargs):
        r = requests.get(
            'https://{env}.saferpay.com/api/{ep}'.format(
                env='www' if self.settings.get('endpoint') == 'live' else 'test',
                ep=endpoint,
            ),
            auth=(self.settings.get('api_user'), self.settings.get('api_pass')),
            *args, **kwargs
        )
        return r

    def get_locale(self, language):
        saferpay_locales = {
            'de', 'en', 'fr', 'da', 'cs', 'es', 'et', 'hr', 'it', 'hu', 'lv', 'lt', 'nl', 'nn',
            'pl', 'pt', 'ru', 'ro', 'sk', 'sl', 'fi', 'sv', 'tr', 'el', 'ja', 'zh'
        }
        if language[:2] in saferpay_locales:
            return language[:2]
        return 'en'

    def _amount_to_decimal(self, cents):
        places = settings.CURRENCY_PLACES.get(self.event.currency, 2)
        return round_decimal(float(cents) / (10 ** places), self.event.currency)

    def _decimal_to_int(self, amount):
        places = settings.CURRENCY_PLACES.get(self.event.currency, 2)
        return int(amount * 10 ** places)

    def _get_payment_page_init_body(self, payment):
        b = {
            "RequestHeader": {
                "SpecVersion": "1.10",
                "CustomerId": self.settings.customer_id,
                "RequestId": str(uuid.uuid4()),
                "RetryIndicator": 0,
                "ClientInfo": {
                    "ShopInfo": "pretix",
                }
            },
            "TerminalId": self.settings.terminal_id,
            "Payment": {
                "Amount": {
                    "Value": str(self._decimal_to_int(payment.amount)),
                    "CurrencyCode": self.event.currency
                },
                "OrderId": "{}-{}-P-{}".format(self.event.slug.upper(), payment.order.code, payment.local_id),
                "Description": "Order {}-{}".format(self.event.slug.upper(), payment.order.code),
                "PayerNote": "{}-{}".format(self.event.slug.upper(), payment.order.code),
            },
            "PaymentMethods": self.payment_methods,
            "Payer": {
                "LanguageCode": self.get_locale(payment.order.locale),
            },
            "ReturnUrls": {
                "Success": build_absolute_uri(self.event, 'plugins:pretix_saferpay:return', kwargs={
                    'order': payment.order.code,
                    'payment': payment.pk,
                    'hash': hashlib.sha1(payment.order.secret.lower().encode()).hexdigest(),
                    'action': 'success'
                }),
                "Fail": build_absolute_uri(self.event, 'plugins:pretix_saferpay:return', kwargs={
                    'order': payment.order.code,
                    'payment': payment.pk,
                    'hash': hashlib.sha1(payment.order.secret.lower().encode()).hexdigest(),
                    'action': 'fail'
                }),
                "Abort": build_absolute_uri(self.event, 'plugins:pretix_saferpay:return', kwargs={
                    'order': payment.order.code,
                    'payment': payment.pk,
                    'hash': hashlib.sha1(payment.order.secret.lower().encode()).hexdigest(),
                    'action': 'abort'
                }),
            },
            "Notification": {
                "NotifyUrl": build_absolute_uri(self.event, 'plugins:pretix_saferpay:webhook', kwargs={
                    'payment': payment.pk,
                }),
            },
            "BillingAddressForm": {
                "Display": False
            },
            "DeliveryAddressForm": {
                "Display": False
            }

        }
        return b

    def execute_payment(self, request: HttpRequest, payment: OrderPayment):
        try:
            req = self._post('Payment/v1/PaymentPage/Initialize', json=self._get_payment_page_init_body(payment))
            req.raise_for_status()
        except HTTPError:
            logger.exception('Saferpay error: %s' % req.text)
            try:
                payment.info_data = req.json()
            except:
                payment.info_data = {
                    'error': True,
                    'detail': req.text
                }
            payment.state = OrderPayment.PAYMENT_STATE_FAILED
            payment.save()
            payment.order.log_action('pretix.event.order.payment.failed', {
                'local_id': payment.local_id,
                'provider': payment.provider,
                'data': payment.info_data
            })
            raise PaymentException(_('We had trouble communicating with Saferpay. Please try again and get in touch '
                                     'with us if this problem persists.'))

        data = req.json()
        payment.info = json.dumps(data)
        payment.state = OrderPayment.PAYMENT_STATE_CREATED
        payment.save()
        request.session['payment_saferpay_order_secret'] = payment.order.secret
        return self.redirect(request, data.get('RedirectUrl'))

    def redirect(self, request, url):
        if request.session.get('iframe_session', False) and self.method in ('paypal', 'sofort', 'giropay', 'paydirekt'):
            signer = signing.Signer(salt='safe-redirect')
            return (
                    build_absolute_uri(request.event, 'plugins:pretix_saferpay:redirect') + '?url=' +
                    urllib.parse.quote(signer.sign(url))
            )
        else:
            return str(url)

    def shred_payment_info(self, obj: OrderPayment):
        if not obj.info:
            return
        d = json.loads(obj.info)
        if 'details' in d:
            d['details'] = {
                k: '█' for k in d['details'].keys()
            }

        d['_shredded'] = True
        obj.info = json.dumps(d)
        obj.save(update_fields=['info'])


class SaferpayCC(SaferpayMethod):
    method = 'creditcard'
    verbose_name = _('Credit card via Saferpay')
    public_name = _('Credit card')

    @property
    def payment_methods(self):
        payment_methods = []
        if self.settings.get('method_visa', as_type=bool):
            payment_methods.append("VISA")
        if self.settings.get('method_diners', as_type=bool):
            payment_methods.append("DINERS")
        if self.settings.get('method_jcb', as_type=bool):
            payment_methods.append("JCB")
        if self.settings.get('method_mastercard', as_type=bool):
            payment_methods.append("MASTERCARD")
        return payment_methods

    @property
    def is_enabled(self) -> bool:
        return self.settings.get('_enabled', as_type=bool) and self.payment_methods


class SaferpayBancontact(SaferpayMethod):
    method = 'bancontact'
    verbose_name = _('Bancontact via Saferpay')
    public_name = _('Bancontact')
    payment_methods = ["BANCONTACT"]


class SaferpayBanktransfer(SaferpayMethod):
    method = 'eprzelewy'
    verbose_name = _('ePrzelewy via Saferpay')
    public_name = _('ePrzelewy')
    payment_methods = ["EPRZELEWY"]


class SaferpayEPS(SaferpayMethod):
    method = 'eps'
    verbose_name = _('EPS via Saferpay')
    public_name = _('eps')
    refunds_allowed = False
    cancel_flow = False
    payment_methods = ["EPS"]


class SaferpayGiropay(SaferpayMethod):
    method = 'giropay'
    verbose_name = _('giropay via Saferpay')
    public_name = _('giropay')
    refunds_allowed = False
    cancel_flow = False
    payment_methods = ["GIROPAY"]


class SaferpayIdeal(SaferpayMethod):
    method = 'ideal'
    verbose_name = _('iDEAL via Saferpay')
    public_name = _('iDEAL')
    refunds_allowed = False
    cancel_flow = False
    payment_methods = ["IDEAL"]


class SaferpayPaydirekt(SaferpayMethod):
    method = 'paydirekt'
    verbose_name = _('paydirekt via Saferpay')
    public_name = _('paydirekt')
    payment_methods = ["PAYDIREKT"]


class SaferpayPayPal(SaferpayMethod):
    method = 'paypal'
    verbose_name = _('PayPal via Saferpay')
    public_name = _('PayPal')
    payment_methods = ["PAYPAL"]


class SaferpayPostfinanceCard(SaferpayMethod):
    method = 'postfinance_card'
    verbose_name = _('PostFinance Card via Saferpay')
    public_name = _('PostFinance Card')
    payment_methods = ["POSTCARD"]


class SaferpayPostfinanceEfinance(SaferpayMethod):
    method = 'postfinance_card'
    verbose_name = _('PostFinance eFinance via Saferpay')
    public_name = _('PostFinance eFinance')
    payment_methods = ["POSTFINANCE"]


class SaferpaySepadebit(SaferpayMethod):
    method = 'sepadebit'
    verbose_name = _('SEPA Direct Debit via Saferpay')
    public_name = _('SEPA Direct Debit')
    refunds_allowed = False
    payment_methods = ["DIRECTDEBIT"]


class SaferpaySofort(SaferpayMethod):
    method = 'sofort'
    verbose_name = _('Sofort via Saferpay')
    public_name = _('Sofort')
    refunds_allowed = False
    cancel_flow = False
    payment_methods = ["SOFORT"]
