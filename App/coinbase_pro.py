import os
import requests
import json
import pandas as pd
from coinbase_auth import CoinbaseAuth

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)


class CoinbasePro():
    def __init__(self, creds, sandbox_mode=True):

        SANDBOX_URL = 'https://api-public.sandbox.pro.coinbase.com/'
        LIVE_URL = 'https://api.pro.coinbase.com/'

        self.creds = creds
        self.sandbox_mode = sandbox_mode
        self.base_url = SANDBOX_URL if sandbox_mode else LIVE_URL
        self.auth = CoinbaseAuth(**self.creds)
        self.load_accounts()

    def load_accounts(self):
        api_json_response = self.api_get('accounts', public=False).json()
        df = pd.DataFrame(api_json_response)
        df.set_index('currency', inplace=True)
        self.account_table = df

    def deposit(self, usd_amount):
        payment_methods = self.api_get('payment-methods', public=False).json()
        bank_accounts = [a for a in payment_methods if a['type'] == 'ach_bank_account']

        first_bank_acct = bank_accounts[0]

        data = {
            "currency": "USD",
            "amount": float(usd_amount),
            "payment_method_id": first_bank_acct['id']
        }
        self.api_post('deposits/payment-method', data=data)

    def api_get(self, endpoint, public, params={}):

        auth = None if public else self.auth

        r = requests.get(**{
            'url': self.base_url + endpoint,
            'auth': auth,
            'params': params,
        })

        if r.status_code != 200:
            print(r.text)
            raise Exception('Api Error: Status Code {}. Text: {}'.format(r.status_code, r.text))

        return r

    def api_post(self, endpoint, params={}, data={}):
        r = requests.post(**{
            'url': self.base_url + endpoint,
            'auth':  self.auth,
            'params': params,
            'data': json.dumps(data),
        })

        if r.status_code != 200:
            print(r.text)
            raise Exception('Api Error: Status Code {}. Text: {}'.format(r.status_code, r.text))

        return r
