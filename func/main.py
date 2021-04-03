# built in
import inspect
# 3rd party
import requests
from cbp_client import AuthAPI
import func.notifications as notify
from func.secrets_manager import get_secret


def event_handler(event, context):

    sandbox_mode = event['sandbox_mode']
    deposit_amount = event['deposit_amount']
    secret_name = 'sandbox/coinbase_pro' if sandbox_mode else 'prod/coinbase_pro'

    secret = get_secret(secret_name)

    api_creds = {key: val
                 for (key, val) in secret.items()
                 if key in ['api_key', 'secret', 'passphrase']}

    payment_name = secret['payment_name']
    api = AuthAPI(credentials=api_creds, sandbox_mode=sandbox_mode)
    payment_id = api.payment_methods(payment_name)['id']

    try:
        r = api.deposit(deposit_amount, payment_method_id=payment_id)
        data = {
            'sandbox_mode': event['sandbox_mode'],
            'specified_amount': event['deposit_amount'],
            'status_code': r.status_code,
            'payment_name': payment_name,
            'text': r.text,
            **r.json()
        }

        _success_email(data, sandbox_mode)

        return data

    except requests.exceptions.HTTPError as e:
        if not sandbox_mode:
            _error_email(
                e=inspect.cleandoc(str(e)),
                payment_name=payment_name,
                payment_id=payment_id,
                deposit_amount=deposit_amount
            )


def _error_email(e, **kwargs):
    msg = inspect.cleandoc('''
        Payment Name: {payment_name}
        Payment ID: {payment_id}
        Amount: ${deposit_amount}
        -----------------------------------------------------
    '''.format(**kwargs))

    notify.email(
        to='terrellvest@gmail.com',
        subject='Failed Coinbase Pro Deposit',
        message=msg + f'\nError:\n{e}'
    )


def _success_email(data, sandbox_mode):
    msg = inspect.cleandoc('''
        Specified Amount: ${specified_amount}
        Deposited Amount: ${amount}
        Deposited From: {payment_name}
        -----------------------------------------------------
    '''.format(**data))
    success_subject = 'Successfull Coinbase Pro Deposit'
    subject = 'SANDBOX MODE | ' + success_subject if sandbox_mode else success_subject
    notify.email(
        to='terrellvest@gmail.com',
        subject=subject,
        message=msg
    )


if __name__ == "__main__":
    event_handler({'sandbox_mode': True, 'desposit_amount': 10}, '')
