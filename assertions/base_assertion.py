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
