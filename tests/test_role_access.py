import pytest

from assertions.base_assertion import assert_error_detail, assert_status_code
from assertions.profile_assertion import (
    assert_profile_exists,
    assert_profile_role,
)
from assertions.role_assertion import (
    assert_profile_id_not_in_list,
    assert_profile_ids_contains,
    assert_profile_ids_only_contains,
    assert_updated_role,
)
from test_data.expected_errors import (
    ONLY_ADMINISTRATORS_CAN_CHANGE_ROLES,
    PERMISSION_DENIED,
)
from tests.helpers import (
    call_api,
    call_api_with_status_retry,
    extract_access_token,
    extract_profile_role,
    extract_profiles,
)


ROLE_ACCESS_CASES = [
    pytest.param(
        "user_credentials",
        "admin_credentials",
        403,
        None,
        PERMISSION_DENIED,
        id="user_cannot_get_admin_profile",
    ),
    pytest.param(
        "admin_credentials",
        "user_credentials",
        200,
        "user",
        None,
        id="admin_can_get_user_profile",
    ),
]


@pytest.mark.parametrize(
    "actor_fixture,target_fixture,expected_status,expected_target_role,expected_error",
    ROLE_ACCESS_CASES,
)
def test_role_access_to_profiles(
    request,
    api_client,
    auth_api,
    user_api,
    account_id_provider,
    actor_fixture,
    target_fixture,
    expected_status,
    expected_target_role,
    expected_error,
):
    actor_credentials = request.getfixturevalue(actor_fixture)
    target_credentials = request.getfixturevalue(target_fixture)
    target_account_id = account_id_provider(target_credentials)

    actor_username, actor_password = actor_credentials
    login_response = call_api("login as actor before role access check", auth_api.login, actor_username, actor_password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    response = call_api(
        "get target profile by account id",
        user_api.get_profile_by_account_id,
        target_account_id,
    )

    assert_status_code(response, expected_status)
    if expected_error:
        assert_error_detail(response, expected_error)
    else:
        assert_profile_exists(response)
        assert_profile_role(response, expected_target_role)


def test_user_list_profiles_does_not_return_foreign_profiles(
    api_client, auth_api, user_api, user_credentials, admin_credentials, account_id_provider
):
    user_id = account_id_provider(user_credentials)
    admin_id = account_id_provider(admin_credentials)
    username, password = user_credentials
    login_response = call_api("login as user before list profiles", auth_api.login, username, password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    response = call_api("list profiles as user", user_api.list_profiles)

    assert_status_code(response, 200)
    profiles = extract_profiles(response)
    profile_ids = [profile["id"] for profile in profiles]
    assert_profile_id_not_in_list(
        profile_ids,
        admin_id,
        "User must not see admin profile in profiles list",
    )
    assert_profile_ids_only_contains(
        profile_ids,
        user_id,
        "User must see only own profile in profiles list",
    )


def test_admin_list_profiles_contains_user_and_admin(
    api_client, auth_api, user_api, user_credentials, admin_credentials, account_id_provider
):
    user_id = account_id_provider(user_credentials)
    admin_id = account_id_provider(admin_credentials)
    username, password = admin_credentials
    login_response = call_api("login as admin before list profiles", auth_api.login, username, password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    response = call_api("list profiles as admin", user_api.list_profiles)

    assert_status_code(response, 200)
    profiles = extract_profiles(response)
    profile_ids = [profile["id"] for profile in profiles]
    assert_profile_ids_contains(
        profile_ids,
        user_id,
        "Admin must see user profile in profiles list",
    )
    assert_profile_ids_contains(
        profile_ids,
        admin_id,
        "Admin must see admin profile in profiles list",
    )


def test_user_cannot_change_own_role(api_client, auth_api, user_api, user_credentials, account_id_provider):
    user_id = account_id_provider(user_credentials)
    username, password = user_credentials
    login_response = call_api("login as user before role update", auth_api.login, username, password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    response = call_api(
        "update own role as user",
        user_api.update_account_role,
        user_id,
        "moderator",
    )

    assert_status_code(response, 403)
    assert_error_detail(response, ONLY_ADMINISTRATORS_CAN_CHANGE_ROLES)


def test_admin_can_change_user_role_and_rollback(
    api_client, auth_api, user_api, user_credentials, admin_credentials, account_id_provider
):
    user_id = account_id_provider(user_credentials)
    admin_username, admin_password = admin_credentials
    login_response = call_api("login as admin before role update", auth_api.login, admin_username, admin_password)
    token = extract_access_token(login_response)

    api_client.set_token(token)
    user_profile_response = call_api(
        "get user profile before role update",
        user_api.get_profile_by_account_id,
        user_id,
    )
    original_role = extract_profile_role(user_profile_response)
    role_was_changed = False

    try:
        update_response = call_api_with_status_retry(
            "change user role to moderator as admin",
            user_api.update_account_role,
            user_id,
            "moderator",
        )
        assert_status_code(update_response, 200)
        role_was_changed = True

        assert_updated_role(update_response, "moderator")
    finally:
        if role_was_changed:
            rollback_response = call_api_with_status_retry(
                "rollback user role after role update test",
                user_api.update_account_role,
                user_id,
                original_role,
            )
            assert_status_code(rollback_response, 200)
