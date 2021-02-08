import os
from pathlib import Path
import json


def pytest_configure(config):
    creds = json.loads(Path('credentials.json').read_text())

    for key, val in creds.items():
        os.environ[key] = val

    os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'coinbase_auto_deposit'
