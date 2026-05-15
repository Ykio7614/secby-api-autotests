import pytest

from assertions.base_assertion import (
    assert_access_token_exists,
    assert_json_schema,
    assert_profile_exists,
    assert_profile_role,
    assert_profile_username,
    assert_error_detail,
    assert_status_code,
    assert_token_is_valid,
    assert_token_type_is_bearer,
)
from models.auth_models import Token
from test_data.expected_errors import INCORRECT_USERNAME_OR_PASSWORD, NOT_AUTHENTICATED
from tests.helpers import call_api, extract_access_token


ROLE_CASES = [
    pytest.param(("user", "USER_USERNAME", "USER_PASSWORD"), id="user"),
    pytest.param(("moderator", "MODERATOR_USERNAME", "MODERATOR_PASSWORD"), id="moderator"),
    pytest.param(("admin", "ADMIN_USERNAME", "ADMIN_PASSWORD"), id="admin"),
]

NEGATIVE_LOGIN_CASES = [
    pytest.param("valid_user", "wrong_password", id="wrong_password"),
    pytest.param("unknown_autotest_user_404", "some_password", id="unknown_user"),
    pytest.param("", "some_password", id="empty_username"),
    pytest.param("valid_user", "", id="empty_password"),
]


def test_user_can_login(auth_api, user_credentials):
    username, password = user_credentials

    response = call_api("login as user", auth_api.login, username, password)

    assert_status_code(response, 200)
    assert_json_schema(response, Token)
    assert_access_token_exists(response)
    assert_token_type_is_bearer(response)


@pytest.mark.parametrize("username_value,password", NEGATIVE_LOGIN_CASES)
def test_user_cannot_login_with_invalid_credentials(
    auth_api, user_credentials, username_value, password
):
    valid_username, _ = user_credentials
    username = valid_username if username_value == "valid_user" else username_value

    response = call_api("login with invalid credentials", auth_api.login, username, password)

    assert_status_code(response, 401)
    assert_error_detail(response, INCORRECT_USERNAME_OR_PASSWORD)


def test_authorized_user_can_get_profile(api_client, auth_api, user_api, user_credentials):
    username, password = user_credentials
    login_response = call_api("login as user before profile request", auth_api.login, username, password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    profile_response = call_api("get user profile", user_api.get_my_profile)

    assert_status_code(profile_response, 200)
    assert_profile_exists(profile_response)


def test_user_cannot_get_profile_without_token(user_api):
    response = call_api("get profile without token", user_api.get_my_profile)

    assert_status_code(response, 403)
    assert_error_detail(response, NOT_AUTHENTICATED)


def test_user_token_can_be_verified(api_client, auth_api, user_credentials):
    username, password = user_credentials
    login_response = call_api("login as user before token verification", auth_api.login, username, password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    verify_response = call_api("verify user token", auth_api.verify)

    assert_status_code(verify_response, 200)
    assert_token_is_valid(verify_response)


def test_token_cannot_be_verified_without_token(auth_api):
    response = call_api("verify token without token", auth_api.verify)

    assert_status_code(response, 403)
    assert_error_detail(response, NOT_AUTHENTICATED)


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
    profile_response = call_api(f"get {role} profile", user_api.get_my_profile)

    assert_status_code(profile_response, 200)
    assert_profile_exists(profile_response)
    assert_profile_username(profile_response, username)
    assert_profile_role(profile_response, role)
