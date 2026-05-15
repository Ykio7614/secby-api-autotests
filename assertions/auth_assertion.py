from assertions.base_assertion import get_json_body


def assert_access_token_exists(response):
    body = get_json_body(response)
    assert body["access_token"], "\n\tAccess token not found in response JSON"


def assert_token_type_is_bearer(response):
    body = get_json_body(response)
    assert body["token_type"] == "bearer", "\n\tInvalid token type in response JSON"


def assert_token_is_valid(response):
    body = get_json_body(response)
    assert body["message"] == "Token is valid", (
        f"\n\tExpected message: Token is valid\n\tActual message: {body['message']}"
    )
    assert "user" in body, "\n\tUser not found in token verification response JSON"
