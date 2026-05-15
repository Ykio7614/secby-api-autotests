import pytest

from assertions.base_assertion import assert_status_code
from assertions.profile_assertion import (
    assert_profile_exists,
    assert_profile_role,
    assert_profile_username,
)
from tests.helpers import call_api, call_api_with_status_retry, extract_access_token


ROLE_CASES = [
    pytest.param(("user", "USER_USERNAME", "USER_PASSWORD"), id="user"),
    pytest.param(("moderator", "MODERATOR_USERNAME", "MODERATOR_PASSWORD"), id="moderator"),
    pytest.param(("admin", "ADMIN_USERNAME", "ADMIN_PASSWORD"), id="admin"),
]


@pytest.mark.parametrize("role_credentials", ROLE_CASES, indirect=True)
def test_role_can_login_and_get_own_profile(
    api_client, auth_api, user_api, role_credentials
):
    role = role_credentials["role"]
    username = role_credentials["username"]
    password = role_credentials["password"]

    login_response = call_api(f"login as {role}", auth_api.login, username, password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    profile_response = call_api_with_status_retry(f"get {role} profile", user_api.get_my_profile)

    assert_status_code(profile_response, 200)
    assert_profile_exists(profile_response)
    assert_profile_username(profile_response, username)
    assert_profile_role(profile_response, role)
