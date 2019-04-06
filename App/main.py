import json
import base64
from coinbase_pro import CoinbasePro
from decrypt import decrypt_symmetric
from storage import download_file


def event_handler(event, context):

    file_str = download_file(
        bucket_name='crypto-manager-keys',
        source_blob_name='coinbase_creds_encrypted.json',
        destination_file='encrypted_creds.json'
    )

    decoded_data_str = base64.b64decode(context['data']).decode('utf-8')
    data = json.loads(decoded_data_str)

    credentials = decrypt_symmetric(**{
        'project_id': 'crypto-manager-235417',
        'location_id': 'us-east4',
        'key_ring_id': 'crypto_manager_cb',
        'crypto_key_id': 'mykey',
        'ciphertext': bytes(file_str)
    })

    if data['action'] == 'live':
        App = CoinbasePro(sandbox_mode=False, creds=credentials['live'])
        App.deposit(25)
        return payload
    else:
        App = CoinbasePro(sandbox_mode=True, creds=credentials['sandbox'])
        return 'coinbase connected ok... no erros'


if __name__ == "__main__":
    print(event_handler({}, {'data': "eyJhY3Rpb24iOiAibGl2ZSJ9"}))
