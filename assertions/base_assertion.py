from typing import Type

from pydantic import BaseModel, ValidationError


def get_json_body(response):
    try:
        return response.json()
    except ValueError as error:
        raise AssertionError(
            f"\n\tResponse body is not valid JSON\n\tActual body: {response.text}"
        ) from error


def assert_status_code(response, expected_status_code):
    assert response.status_code == expected_status_code, (
        f"\n\tExpected status code: {expected_status_code}\n\tActual status code: {response.status_code}"
    )

def assert_json_schema(response, model:Type[BaseModel]):
    body = get_json_body(response)
    try:
        if isinstance(body, list):
            for item in body:
                model.model_validate(item, strict=True)
        else:
            model.model_validate(body, strict=True)
    except ValidationError as error:
        raise AssertionError(
            f"\n\tResponse JSON does not match schema: {model.__name__}\n\tValidation error: {error}"
        ) from error
    


def assert_left_in_right_json(left, right):
    for key, value in left.items():
        assert key in right, f"\n\tKey '{key}' not found in response JSON"
        assert right[key] == value, (
            f"\n\tExpected value for key '{key}': {value}\n\tActual value: {right[key]}"
        )


def assert_error_detail(response, expected_detail):
    body = get_json_body(response)
    actual_detail = body.get("detail")
    assert actual_detail == expected_detail, (
        f"\n\tExpected error detail: {expected_detail}\n\tActual error detail: {actual_detail}"
    )
