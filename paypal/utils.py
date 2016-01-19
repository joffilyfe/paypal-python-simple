SANDBOX_AUTH_URL = 'https://api.sandbox.paypal.com/v1/oauth2/token'
SANDBOX_CHECKOUT_URL = 'https://api.sandbox.paypal.com/v1/payments/payment'

LIVE_AUTH_URL = 'https://api.paypal.com/v1/oauth2/token'
LIVE_CHECKOUT_URL = 'https://api.paypal.com/v1/payments/payment'


def auth_header():
    header = {}
    header['Accept'] = 'application/json'
    header['Accept-Language'] = 'en_US'

    return header


def checkout_header(access_token):

    header = {}
    header['Content-Type'] = 'application/json'
    header['Authorization'] = 'Bearer {}'.format(access_token)

    return header
