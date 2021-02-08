import os
import boto3
from base64 import b64decode


def decrypt(encrypted_val):
    return boto3.client(
        service_name='kms'
    ).decrypt(
        CiphertextBlob=b64decode(encrypted_val),
        EncryptionContext={
            'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']
        }
    )['Plaintext'].decode('utf-8')
