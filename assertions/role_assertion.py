from assertions.base_assertion import get_json_body


def assert_profile_id_not_in_list(profile_ids, forbidden_profile_id, message):
    assert forbidden_profile_id not in profile_ids, (
        f"\n\t{message}\n\tForbidden profile id: {forbidden_profile_id}"
        f"\n\tActual profile ids: {profile_ids}"
    )


def assert_profile_ids_contains(profile_ids, expected_profile_id, message):
    assert expected_profile_id in profile_ids, (
        f"\n\t{message}\n\tExpected profile id: {expected_profile_id}"
        f"\n\tActual profile ids: {profile_ids}"
    )


def assert_profile_ids_only_contains(profile_ids, expected_profile_id, message):
    assert all(profile_id == expected_profile_id for profile_id in profile_ids), (
        f"\n\t{message}\n\tExpected only profile id: {expected_profile_id}"
        f"\n\tActual profile ids: {profile_ids}"
    )


def assert_updated_role(response, expected_role):
    body = get_json_body(response)
    actual_role = body["new_role"]
    assert actual_role == expected_role, (
        f"\n\tExpected new role: {expected_role}\n\tActual new role: {actual_role}"
    )
