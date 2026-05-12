from typing import Type

from pydantic import BaseModel


def assert_status_code(response, expected_status_code):
    assert response.status_code == expected_status_code, (
        f"\n\tExpected status code: {expected_status_code}\n\tActual status code: {response.status_code}"
    )

def assert_json_schema(response, model:Type[BaseModel]):
    body = response.json()
    if isinstance(body, list):
        for item in body:
            model.model_validate(item, strict=True)
    else:
        model.model_validate(body, strict=True)
    


def assert_left_in_right_json(left, right):
    for key, value in left.items():
        assert key in right, f"\n\tKey '{key}' not found in response JSON"
        assert right[key] == value, (
            f"\n\tExpected value for key '{key}': {value}\n\tActual value: {right[key]}"
        )


def assert_access_token_exists(response):
    body = response.json()
    assert body["access_token"], "\n\tAccess token not found in response JSON"


def assert_token_type_is_bearer(response):
    body = response.json()
    assert body["token_type"] == "bearer", "\n\tInvalid token type in response JSON"


def assert_profile_exists(response):
    body = response.json()
    assert "profile" in body, "\n\tProfile not found in response JSON"


def assert_profile_role(response, expected_role):
    body = response.json()
    actual_role = body["profile"]["role"]["name"]
    assert actual_role == expected_role, (
        f"\n\tExpected profile role: {expected_role}\n\tActual profile role: {actual_role}"
    )


def assert_profile_username(response, expected_username):
    body = response.json()
    actual_username = body["profile"]["username"]
    assert actual_username == expected_username, (
        f"\n\tExpected profile username: {expected_username}\n\tActual profile username: {actual_username}"
    )


def assert_token_is_valid(response):
    body = response.json()
    assert body["message"] == "Token is valid", (
        f"\n\tExpected message: Token is valid\n\tActual message: {body['message']}"
    )
    assert "user" in body, "\n\tUser not found in token verification response JSON"
