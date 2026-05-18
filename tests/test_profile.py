import os

from assertions.base_assertion import assert_error_detail, assert_json_schema, assert_status_code
from assertions.profile_assertion import (
    assert_profile_email,
    assert_profile_exists,
    assert_profile_username,
)
from models.profile_models import UserProfileResponse
from test_data.expected_errors import NOT_AUTHENTICATED
from tests.helpers import call_api, extract_access_token, extract_user_email


def test_authorized_user_can_get_profile(api_client, auth_api, user_api, user_credentials):
    username, password = user_credentials
    login_response = call_api("login as user before profile request", auth_api.login, username, password)
    token = extract_access_token(login_response)
    expected_email = os.getenv("USER_EMAIL")

    api_client.set_token(token)
    profile_response = call_api("get user profile", user_api.get_my_profile)

    assert_status_code(profile_response, 200)
    assert_json_schema(profile_response, UserProfileResponse)
    assert_profile_exists(profile_response)
    assert_profile_username(profile_response, username)
    assert_profile_email(profile_response, expected_email)


def test_user_cannot_get_profile_without_token(user_api):
    response = call_api("get profile without token", user_api.get_my_profile)

    assert_status_code(response, 403)
    assert_error_detail(response, NOT_AUTHENTICATED)
