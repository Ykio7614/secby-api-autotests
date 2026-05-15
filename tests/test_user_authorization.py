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


def test_user_can_login(auth_api, user_credentials):
    username, password = user_credentials

    response = auth_api.login(username, password)

    assert_status_code(response, 200)
    assert_json_schema(response, Token)
    assert_access_token_exists(response)
    assert_token_type_is_bearer(response)


def test_user_cannot_login_with_invalid_password(auth_api, user_credentials):
    username, _ = user_credentials

    response = auth_api.login(username, "wrong_password")

    assert_status_code(response, 401)
    assert_error_detail(response, INCORRECT_USERNAME_OR_PASSWORD)


def test_authorized_user_can_get_profile(api_client, auth_api, user_api, user_credentials):
    username, password = user_credentials
    login_response = auth_api.login(username, password)
    token = login_response.json()["access_token"]

    api_client.set_token(token)
    profile_response = user_api.get_my_profile()

    assert_status_code(profile_response, 200)
    assert_profile_exists(profile_response)


def test_user_cannot_get_profile_without_token(user_api):
    response = user_api.get_my_profile()

    assert_status_code(response, 403)
    assert_error_detail(response, NOT_AUTHENTICATED)


def test_authorized_user_profile_has_expected_username_and_role(
    api_client, auth_api, user_api, user_credentials
):
    username, password = user_credentials
    login_response = auth_api.login(username, password)
    token = login_response.json()["access_token"]

    api_client.set_token(token)
    profile_response = user_api.get_my_profile()

    assert_status_code(profile_response, 200)
    assert_profile_username(profile_response, username)
    assert_profile_role(profile_response, "user")


def test_user_token_can_be_verified(api_client, auth_api, user_credentials):
    username, password = user_credentials
    login_response = auth_api.login(username, password)
    token = login_response.json()["access_token"]

    api_client.set_token(token)
    verify_response = auth_api.verify()

    assert_status_code(verify_response, 200)
    assert_token_is_valid(verify_response)


def test_token_cannot_be_verified_without_token(auth_api):
    response = auth_api.verify()

    assert_status_code(response, 403)
    assert_error_detail(response, NOT_AUTHENTICATED)


def test_authorized_admin_can_get_profile(api_client, auth_api, user_api, admin_credentials):
    username, password = admin_credentials
    login_response = auth_api.login(username, password)
    token = login_response.json()["access_token"]

    api_client.set_token(token)
    profile_response = user_api.get_my_profile()

    assert_status_code(profile_response, 200)
    assert_profile_exists(profile_response)
    assert_profile_role(profile_response, "admin")


def test_authorized_admin_profile_has_expected_username_and_role(
    api_client, auth_api, user_api, admin_credentials
):
    username, password = admin_credentials
    login_response = auth_api.login(username, password)
    token = login_response.json()["access_token"]

    api_client.set_token(token)
    profile_response = user_api.get_my_profile()

    assert_status_code(profile_response, 200)
    assert_profile_username(profile_response, username)
    assert_profile_role(profile_response, "admin")
