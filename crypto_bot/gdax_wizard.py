import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from decimal import Decimal
import time


# Real API credentials
#API_KEY = 'c1742ed7bfb6733757a9c3cf9eff6db9'
#API_SECRET = 'Gq4/0R4RiUDUBX70aMFVd/LayzghusySCooQJfwZgx62Loz+3/nBJU3Ycw8ftnpZ9t2Ac/jJcMtVP7x/h9q4tA=='
#API_PASS = 'crypto_bot'
#api_url = 'https://api.gdax.com/accounts'#base64.b64encode(b'https://api.gdax.com/accounts')

# Sandbox API credentials
SB_API_KEY = '90d71b9cbeb4302747186162c590ceb4'
SB_API_SECRET = 'jprLxcho99Fj+04nqhOAoqehyAF3Lxo3uWCXkF7/UB6J32a0kgo0T0hY0Yh6v6QNN69H3IK05hieCaAJs1s8kw=='
SB_API_PASS = 'sandbox_crypto_bot'
sb_api_url = 'https://api-public.sandbox.gdax.com'

# Create custom authentication for Exchange
class GDAXRequestAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

def place_order(symbol, side, product_id, amount):
    sb_auth = GDAXRequestAuth(SB_API_KEY, SB_API_SECRET, SB_API_PASS)
    order_url = sb_api_url + '/orders'
    order_data = {
        'type': symbol,
        'side': side,
        'product_id': product_id,
        'size': amount
    }
    response = requests.post(order_url, data=json.dumps(order_data), auth=sb_auth)
    print(response.json())

def get_btc_price():
    while(True):
        sb_auth = GDAXRequestAuth(SB_API_KEY, SB_API_SECRET, SB_API_PASS)
        price_url = sb_api_url + '/products/BTC-USD/ticker'
        price_url = 'https://api.neuryx.com/api/price/btc'
        response = requests.get(price_url)
        price = float(response.json()['btc_price']['price'])
        price = round(price,2)
        print(price)
        time.sleep(.5)



def sell_all_btc():
    pass

def buy_max_btc():
    pass

def test():
    #place_order('market', 'buy', 'BTC-USD', '0.01')
    #place_order('market', 'sell', 'BTC-USD', '0.01')
    get_btc_price()
