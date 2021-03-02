from cbp_client import AuthAPI
from func.secrets_manager import get_secrets


def event_handler(event, context):

    sandbox_mode = event['sandbox_mode']
    deposit_amount = event['deposit_amount']

    all_secrets = get_secrets()
    secrets = (all_secrets.sandbox
               if sandbox_mode
               else all_secrets.live)

    creds = {key: val
             for (key, val) in secrets._asdict().items()
             if key in ['api_key', 'secret', 'passphrase']}

    payment_name = secrets.payment_name

    api = AuthAPI(credentials=creds, sandbox_mode=sandbox_mode)

    payment_id = api.payment_methods(payment_name)['id']

    r = api.deposit(deposit_amount, payment_method_id=payment_id)

    return r.json()


if __name__ == "__main__":
    event_handler({'sandbox_mode': True, 'desposit_amount': 10}, '')
