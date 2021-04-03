import os


def pytest_configure(config):

    # set lambda function name as environment variable
    os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'coinbase_auto_deposit'
