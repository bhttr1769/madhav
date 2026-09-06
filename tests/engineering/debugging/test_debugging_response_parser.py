import json

import pytest

from brain.engineering.debugging.debugging_response_parser import (
    DebuggingResponseParser,
)
from brain.engineering.debugging.models.debugging_result import (
    DebuggingResult,
)


def valid_response():
    return json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": "return fixed_value",
                }
            ],
            "diagnosis": "The failure was caused by an undefined variable.",
        }
    )


def test_parser_returns_debugging_result():
    result = DebuggingResponseParser.parse(
        valid_response()
    )

    assert isinstance(result, DebuggingResult)
    assert len(result.changes) == 1
    assert result.changes[0].path == "brain/example.py"
    assert result.changes[0].operation == "modify"
    assert result.diagnosis == (
        "The failure was caused by an undefined variable."
    )


def test_parser_returns_immutable_changes():
    result = DebuggingResponseParser.parse(
        valid_response()
    )

    assert isinstance(result.changes, tuple)


def test_parser_rejects_non_string_response():
    with pytest.raises(TypeError):
        DebuggingResponseParser.parse(None)


def test_parser_rejects_invalid_json():
    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            "not valid json"
        )


def test_parser_rejects_non_object_json():
    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(["changes"])
        )


def test_parser_rejects_wrong_top_level_keys():
    payload = {
        "changes": [],
        "diagnosis": "Failure diagnosed.",
        "extra": "unexpected",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_missing_top_level_key():
    payload = {
        "changes": [],
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_list_changes():
    payload = {
        "changes": {},
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_string_diagnosis():
    payload = {
        "changes": [],
        "diagnosis": 123,
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_empty_diagnosis():
    payload = {
        "changes": [],
        "diagnosis": "   ",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_object_change():
    payload = {
        "changes": ["invalid"],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_wrong_change_keys():
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": "modify",
                "content": "fixed",
                "extra": "unexpected",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_string_change_fields():
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": "modify",
                "content": 123,
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_unsupported_operation():
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": "rename",
                "content": "fixed",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_normalizes_operation():
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": "MODIFY",
                "content": "fixed",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    result = DebuggingResponseParser.parse(
        json.dumps(payload)
    )

    assert result.changes[0].operation == "modify"


def test_parser_rejects_absolute_path():
    payload = {
        "changes": [
            {
                "path": "/brain/example.py",
                "operation": "modify",
                "content": "fixed",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_parent_directory_traversal():
    payload = {
        "changes": [
            {
                "path": "../example.py",
                "operation": "modify",
                "content": "fixed",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_duplicate_paths():
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": "modify",
                "content": "first",
            },
            {
                "path": "brain/example.py",
                "operation": "modify",
                "content": "second",
            },
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_allows_empty_changes():
    payload = {
        "changes": [],
        "diagnosis": "No code changes are required.",
    }

    result = DebuggingResponseParser.parse(
        json.dumps(payload)
    )

    assert result.changes == ()


@pytest.mark.parametrize(
    "operation",
    ["create", "modify"],
)
def test_parser_rejects_empty_content_for_write_operations(
    operation,
):
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": operation,
                "content": "   ",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    with pytest.raises(ValueError):
        DebuggingResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_allows_empty_content_for_delete():
    payload = {
        "changes": [
            {
                "path": "brain/example.py",
                "operation": "delete",
                "content": "",
            }
        ],
        "diagnosis": "Failure diagnosed.",
    }

    result = DebuggingResponseParser.parse(
        json.dumps(payload)
    )

    assert result.changes[0].operation == "delete"
    assert result.changes[0].content == ""