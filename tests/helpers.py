import pytest
import time
from httpx import HTTPError


def call_api(action, method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except HTTPError as error:
        pytest.fail(f"API request failed during '{action}': {error}")


def call_api_with_status_retry(action, method, *args, **kwargs):
    retry_statuses = kwargs.pop("retry_statuses", (503,))
    attempts = kwargs.pop("attempts", 5)
    delay = kwargs.pop("delay", 1)
    response = None

    for attempt in range(attempts):
        response = call_api(action, method, *args, **kwargs)
        if response.status_code not in retry_statuses:
            return response
        if attempt < attempts - 1:
            time.sleep(delay)

    return response


def extract_access_token(response):
    try:
        body = response.json()
        return body["access_token"]
    except ValueError:
        pytest.fail(f"Login response is not valid JSON: {response.text}")
    except KeyError:
        pytest.fail(f"Login response does not contain access_token: {response.text}")


def extract_profile(response):
    try:
        body = response.json()
        return body["profile"]
    except ValueError:
        pytest.fail(f"Profile response is not valid JSON: {response.text}")
    except KeyError:
        pytest.fail(f"Profile response does not contain profile: {response.text}")


def extract_account_id(response):
    profile = extract_profile(response)
    try:
        return profile["id"]
    except KeyError:
        pytest.fail(f"Profile response does not contain account id: {response.text}")


def extract_profiles(response):
    try:
        body = response.json()
        return body["profiles"]
    except ValueError:
        pytest.fail(f"Profiles response is not valid JSON: {response.text}")
    except KeyError:
        pytest.fail(f"Profiles response does not contain profiles: {response.text}")


def extract_profile_role(response):
    profile = extract_profile(response)
    try:
        return profile["role"]["name"]
    except KeyError:
        pytest.fail(f"Profile response does not contain role name: {response.text}")
