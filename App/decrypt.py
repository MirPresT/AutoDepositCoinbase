import json
from google.cloud import kms_v1


def decrypt_symmetric(
    project_id, location_id, key_ring_id,
    crypto_key_id, ciphertext
):
    """Decrypts input ciphertext using the provided symmetric CryptoKey."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    name = client.crypto_key_path_path(
        project_id, location_id,
        key_ring_id, crypto_key_id
    )

    # Use the KMS API to decrypt the data.
    response = client.decrypt(name, ciphertext)
    return json.loads(response.plaintext)
