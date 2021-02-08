import os
from cbp_client import AuthAPI
from func.decrypt import decrypt


SANDBOX_CREDENTIALS = {
    'secret': decrypt(os.environ['sandbox_secret']),
    'passphrase': decrypt(os.environ['sandbox_passphrase']),
    'api_key': os.environ['sandbox_api_key']
}

LIVE_CREDENTIALS = {
    'secret': decrypt(os.environ['secret']),
    'passphrase': decrypt(os.environ['passphrase']),
    'api_key': os.environ['api_key']
}


def event_handler(event, context):

    sandbox_mode = event['sandbox_mode']
    deposit_amount = event['deposit_amount']

    if sandbox_mode:
        credentials = SANDBOX_CREDENTIALS
        payment_method_name = decrypt(os.environ['sandbox_bank_name'])
    else:
        credentials = LIVE_CREDENTIALS
        payment_method_name = decrypt(os.environ['primary_bank_name'])

    api = AuthAPI(credentials=credentials, sandbox_mode=sandbox_mode)

    payment_method_id = api.payment_methods(payment_method_name)['id']

    return api.deposit(deposit_amount, payment_method_id=payment_method_id)


if __name__ == "__main__":
    event_handler('', '')
