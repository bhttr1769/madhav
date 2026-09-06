import json

import pytest

from brain.engineering.refactoring.refactoring_response_parser import (
    RefactoringResponseParser,
)
from brain.engineering.refactoring.models.refactoring_result import (
    RefactoringResult,
)


def valid_response():
    return json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": "return value",
                }
            ],
            "rationale": (
                "The implementation can be simplified "
                "without changing behavior."
            ),
        }
    )


def test_parser_returns_refactoring_result():
    result = RefactoringResponseParser.parse(
        valid_response()
    )

    assert isinstance(result, RefactoringResult)
    assert len(result.changes) == 1
    assert result.changes[0].path == "brain/example.py"
    assert result.changes[0].operation == "modify"
    assert result.rationale == (
        "The implementation can be simplified "
        "without changing behavior."
    )


def test_parser_returns_immutable_changes():
    result = RefactoringResponseParser.parse(
        valid_response()
    )

    assert isinstance(result.changes, tuple)


def test_parser_rejects_non_string_response():
    with pytest.raises(TypeError):
        RefactoringResponseParser.parse(None)


def test_parser_rejects_invalid_json():
    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            "not valid json"
        )


def test_parser_rejects_non_object_json():
    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(["changes"])
        )


def test_parser_rejects_wrong_top_level_keys():
    payload = {
        "changes": [],
        "rationale": "Valid rationale.",
        "extra": "unexpected",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_missing_top_level_key():
    payload = {
        "changes": [],
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_list_changes():
    payload = {
        "changes": {},
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_string_rationale():
    payload = {
        "changes": [],
        "rationale": 123,
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_empty_rationale():
    payload = {
        "changes": [],
        "rationale": "   ",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_rejects_non_object_change():
    payload = {
        "changes": ["invalid"],
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    result = RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
            json.dumps(payload)
        )


def test_parser_allows_empty_changes():
    payload = {
        "changes": [],
        "rationale": (
            "No refactoring is justified for this implementation."
        ),
    }

    result = RefactoringResponseParser.parse(
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
        "rationale": "Valid rationale.",
    }

    with pytest.raises(ValueError):
        RefactoringResponseParser.parse(
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
        "rationale": "The obsolete file can be removed.",
    }

    result = RefactoringResponseParser.parse(
        json.dumps(payload)
    )

    assert result.changes[0].operation == "delete"
    assert result.changes[0].content == ""