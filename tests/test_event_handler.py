from func.main import event_handler
import pytest
import json


@pytest.fixture
def fake_event():
    return {
        'sandbox_mode': True,
        'deposit_amount': 10
    }


@pytest.fixture
def fake_context():
    return {
        "function_name": "sample-function-name",
        "function_version ": "0.1.1",
        "invoked_function_arn ": 'arn:aws:events:us-east-1:123456789012',
        "memory_limit_in_mb ": "500",
        "aws_request_id ": "id",
        "log_group_name ": "na",
        "log_stream_name ": "na",
        "resources": [
            "arn:aws:events:us-east-1:123456789012:rule/my-schedule"
        ]
    }


def test_event_handler(fake_event, fake_context):

    r = event_handler(fake_event, fake_context)

    assert isinstance(r, dict)
    assert json.dumps(r)
    assert r['status_code'] == 200
    print(json.dumps(r, indent=4))
