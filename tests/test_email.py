import json

# 3rd party
import pytest
from func import notifications as notify


def test_email():
    notify.email(
        subject='Email Module Can Send Emails',
        message='body of email...',
        to='terrellvest+trash/test@gmail.com'
    )
