import requests
import json
from . import utils


class PaypalSandBoxConf(object):

    def __init__(self):
        self.auth_url = utils.SANDBOX_AUTH_URL
        self.checkout_url = utils.SANDBOX_CHECKOUT_URL
        self.currency = 'BRL'


class PaypalLiveConf(object):

    def __init__(self):
        self.auth_url = utils.LIVE_AUTH_URL
        self.checkout_url = utils.LIVE_CHECKOUT_URL
        self.currency = 'BRL'


class PaypalAuthResponse(object):
    ''' Parse PayPal byte response to dict with access_token '''

    def __init__(self, content=None):
        self.content = content
        self.token = None
        self.parse_bytes()

    def parse_bytes(self):
        string = self.content.decode('utf-8')
        content = json.loads(string)
        self.token = content['access_token']


class PayalCheckoutResponse(object):
    ''' Parse PayPal checkout response '''

    def __init__(self, content=None):
        self.content = content
        self.url = None
        self.id = None
        self.status = None
        self.parse_bytes()

    def parse_bytes(self):
        string = self.content.decode('utf-8')
        string = json.loads(string)

        self.id = string.get('id')
        self.state = string.get('state')

        for url in string.get('links'):
            if url.get('method') == 'REDIRECT':
                self.url = url.get('href')


class PaypalAuthorize(object):
    ''' Authorize your app in PayPal API '''

    def __init__(self, config=None, client=None, secret=None):
        if config is None:
            self.config = PaypalLiveConf()
        else:
            self.config = config
        self.headers = utils.auth_header()
        self.client = client
        self.secret = secret
        self.content = None
        self.authorize()

    def authorize(self):
        data = {'grant_type': 'client_credentials'}
        response = requests.post(self.config.auth_url, headers=self.headers,
                                 auth=(self.client, self.secret), data=data)

        if response.status_code == 200:
            self.content = PaypalAuthResponse(response.content)
        else:
            raise Exception('Unauthorized. Status: %i' % response.status_code)


class Paypal(object):
    '''
    @config = Configuration object
    @auth = Authorization object
    '''

    def __init__(self, config=None, auth=None):
        if config is None:
            self.config = PaypalLiveConf()
        else:
            self.config = config
        self.access_token = auth.content.token
        self.headers = utils.checkout_header(self.access_token)
        self.intent = 'sale'
        self.method = 'paypal'
        self.return_url = ''
        self.cancel_url = ''
        self.price = ''
        self.response = None

    def build_data(self):
        ''' Build data for express checkout method '''
        data = {}
        data['intent'] = self.intent
        data['payer'] = {'payment_method': self.method}
        data['redirect_urls'] = {
            'return_url': self.return_url,
            'cancel_url': self.cancel_url,
        }

        data['transactions'] = [{
            'amount': {
                'total': self.price,
                'currency': self.config.currency,
                'details': {
                    'subtotal': self.price,
                }
            },
            'description': 'decricao'
        }]

        return json.dumps(data)

    def checkout(self):
        ''' Simple express checkout with paypal method '''
        headers = utils.checkout_header(self.access_token)
        data = self.build_data()

        response = requests.post(self.config.checkout_url,
                                 headers=headers, data=self.build_data())

        if response.status_code == 201:
            parse = PayalCheckoutResponse(content=response.content)
            return parse
        else:
            self.response = None
            raise Exception('Error at checkout')
