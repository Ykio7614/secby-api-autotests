from assertions.base_assertion import get_json_body


def assert_profile_exists(response):
    body = get_json_body(response)
    assert "profile" in body, "\n\tProfile not found in response JSON"


def assert_profile_role(response, expected_role):
    body = get_json_body(response)
    actual_role = body["profile"]["role"]["name"]
    assert actual_role == expected_role, (
        f"\n\tExpected profile role: {expected_role}\n\tActual profile role: {actual_role}"
    )


def assert_profile_username(response, expected_username):
    body = get_json_body(response)
    actual_username = body["profile"]["username"]
    assert actual_username == expected_username, (
        f"\n\tExpected profile username: {expected_username}\n\tActual profile username: {actual_username}"
    )


def assert_profile_email(response, expected_email):
    body = get_json_body(response)
    actual_email = body["profile"]["email"]
    assert actual_email == expected_email, (
        f"\n\tExpected profile email: {expected_email}\n\tActual profile email: {actual_email}"
    )
