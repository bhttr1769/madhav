import json

import pytest

from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult as GenerationResult,
)

from brain.engineering.testing.test_generation_response_parser import (
    TestGenerationResponseParser as ResponseParser,
)


def valid_response() -> str:
    return json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "create",
                    "content": "def test_health():\n    pass",
                }
            ]
        }
    )


def test_parse_returns_generation_result():
    result = ResponseParser.parse(valid_response())

    assert isinstance(result, GenerationResult)


def test_parse_preserves_change():
    result = ResponseParser.parse(valid_response())

    assert len(result.changes) == 1

    change = result.changes[0]

    assert change.path == "tests/test_health.py"
    assert change.operation == "create"
    assert change.content == "def test_health():\n    pass"


def test_parse_returns_empty_changes():
    result = ResponseParser.parse(
        json.dumps({"changes": []})
    )

    assert result.changes == ()


def test_parse_rejects_non_string_response():
    with pytest.raises(TypeError):
        ResponseParser.parse({})


def test_parse_rejects_invalid_json():
    with pytest.raises(ValueError):
        ResponseParser.parse("{invalid")


def test_parse_rejects_non_object_json():
    with pytest.raises(ValueError):
        ResponseParser.parse("[]")


def test_parse_rejects_missing_changes():
    with pytest.raises(ValueError):
        ResponseParser.parse("{}")


def test_parse_rejects_extra_top_level_fields():
    response = json.dumps(
        {
            "changes": [],
            "decision": {},
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_non_list_changes():
    response = json.dumps(
        {
            "changes": {},
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_non_object_change():
    response = json.dumps(
        {
            "changes": ["invalid"],
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_missing_change_field():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "create",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_extra_change_field():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "create",
                    "content": "test",
                    "extra": "invalid",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "field",
    [
        "path",
        "operation",
        "content",
    ],
)
def test_parse_rejects_non_string_change_fields(field):
    change = {
        "path": "tests/test_health.py",
        "operation": "create",
        "content": "test",
    }

    change[field] = 123

    response = json.dumps(
        {
            "changes": [change],
        }
    )

    with pytest.raises(TypeError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_path():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "",
                    "operation": "create",
                    "content": "test",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_operation():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "",
                    "content": "test",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "operation",
    [
        "create",
        "modify",
        "delete",
    ],
)
def test_parse_accepts_supported_operations(operation):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": operation,
                    "content": "test",
                }
            ]
        }
    )

    result = ResponseParser.parse(response)

    assert result.changes[0].operation == operation


def test_parse_normalizes_operation_case():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "CREATE",
                    "content": "test",
                }
            ]
        }
    )

    result = ResponseParser.parse(response)

    assert result.changes[0].operation == "create"


def test_parse_rejects_unsupported_operation():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "replace",
                    "content": "test",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "path",
    [
        "/tests/test_health.py",
        "\\tests\\test_health.py",
    ],
)
def test_parse_rejects_absolute_path(path):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": path,
                    "operation": "create",
                    "content": "test",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "path",
    [
        "../test_health.py",
        "tests/../test_health.py",
        "tests\\..\\test_health.py",
    ],
)
def test_parse_rejects_parent_traversal(path):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": path,
                    "operation": "create",
                    "content": "test",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_duplicate_paths():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "create",
                    "content": "test",
                },
                {
                    "path": "tests/test_health.py",
                    "operation": "modify",
                    "content": "test",
                },
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "operation",
    [
        "create",
        "modify",
    ],
)
def test_parse_rejects_empty_content_for_create_and_modify(
    operation,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": operation,
                    "content": "   ",
                }
            ]
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_allows_empty_content_for_delete():
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "delete",
                    "content": "",
                }
            ]
        }
    )

    result = ResponseParser.parse(response)

    assert result.changes[0].content == ""