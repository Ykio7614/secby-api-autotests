import pytest
from httpx import HTTPError


def call_api(action, method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except HTTPError as error:
        pytest.fail(f"API request failed during '{action}': {error}")


def extract_access_token(response):
    try:
        body = response.json()
        return body["access_token"]
    except ValueError:
        pytest.fail(f"Login response is not valid JSON: {response.text}")
    except KeyError:
        pytest.fail(f"Login response does not contain access_token: {response.text}")
