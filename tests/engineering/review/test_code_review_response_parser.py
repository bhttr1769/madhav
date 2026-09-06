import json

import pytest

from brain.engineering.review.code_review_response_parser import (
    CodeReviewResponseParser as ResponseParser,
)

from brain.engineering.review.models.code_review_result import (
    CodeReviewResult as ReviewResult,
)


def valid_response() -> str:
    return json.dumps(
        {
            "approved": False,
            "findings": [
                {
                    "severity": "high",
                    "category": "correctness",
                    "path": "brain/example.py",
                    "message": "Incorrect behavior.",
                    "recommendation": "Fix the implementation.",
                }
            ],
            "summary": "The implementation requires correction.",
        }
    )


def test_parse_returns_review_result():
    result = ResponseParser.parse(valid_response())

    assert isinstance(result, ReviewResult)


def test_parse_preserves_approval():
    result = ResponseParser.parse(valid_response())

    assert result.approved is False


def test_parse_preserves_finding():
    result = ResponseParser.parse(valid_response())

    assert len(result.findings) == 1

    finding = result.findings[0]

    assert finding.severity == "high"
    assert finding.category == "correctness"
    assert finding.path == "brain/example.py"
    assert finding.message == "Incorrect behavior."
    assert finding.recommendation == "Fix the implementation."


def test_parse_preserves_summary():
    result = ResponseParser.parse(valid_response())

    assert result.summary == (
        "The implementation requires correction."
    )


def test_parse_accepts_approved_review():
    response = json.dumps(
        {
            "approved": True,
            "findings": [],
            "summary": "The implementation is acceptable.",
        }
    )

    result = ResponseParser.parse(response)

    assert result.approved is True
    assert result.findings == ()


def test_parse_accepts_empty_findings():
    response = json.dumps(
        {
            "approved": True,
            "findings": [],
            "summary": "No issues found.",
        }
    )

    result = ResponseParser.parse(response)

    assert result.findings == ()


def test_parse_rejects_non_string_response():
    with pytest.raises(TypeError):
        ResponseParser.parse({})


def test_parse_rejects_invalid_json():
    with pytest.raises(ValueError):
        ResponseParser.parse("{invalid")


def test_parse_rejects_non_object_json():
    with pytest.raises(ValueError):
        ResponseParser.parse("[]")


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {
            "approved": True,
            "findings": [],
        },
        {
            "approved": True,
            "findings": [],
            "summary": "ok",
            "extra": "invalid",
        },
    ],
)
def test_parse_rejects_invalid_top_level_schema(payload):
    with pytest.raises(ValueError):
        ResponseParser.parse(json.dumps(payload))


@pytest.mark.parametrize(
    "approved",
    [
        "true",
        1,
        0,
        None,
        [],
        {},
    ],
)
def test_parse_rejects_non_boolean_approved(approved):
    response = json.dumps(
        {
            "approved": approved,
            "findings": [],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(TypeError):
        ResponseParser.parse(response)


def test_parse_rejects_non_list_findings():
    response = json.dumps(
        {
            "approved": True,
            "findings": {},
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "summary",
    [
        123,
        None,
        [],
        {},
    ],
)
def test_parse_rejects_non_string_summary(summary):
    response = json.dumps(
        {
            "approved": True,
            "findings": [],
            "summary": summary,
        }
    )

    with pytest.raises(TypeError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_summary():
    response = json.dumps(
        {
            "approved": True,
            "findings": [],
            "summary": "   ",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_non_object_finding():
    response = json.dumps(
        {
            "approved": False,
            "findings": ["invalid"],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_missing_finding_field():
    response = json.dumps(
        {
            "approved": False,
            "findings": [
                {
                    "severity": "high",
                    "category": "correctness",
                    "path": "brain/example.py",
                    "message": "Problem.",
                }
            ],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_extra_finding_field():
    response = json.dumps(
        {
            "approved": False,
            "findings": [
                {
                    "severity": "high",
                    "category": "correctness",
                    "path": "brain/example.py",
                    "message": "Problem.",
                    "recommendation": "Fix it.",
                    "extra": "invalid",
                }
            ],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "field",
    [
        "severity",
        "category",
        "path",
        "message",
        "recommendation",
    ],
)
def test_parse_rejects_non_string_finding_fields(field):
    finding = {
        "severity": "high",
        "category": "correctness",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    finding[field] = 123

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(TypeError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "severity",
    [
        "critical",
        "high",
        "medium",
        "low",
    ],
)
def test_parse_accepts_supported_severity(severity):
    finding = {
        "severity": severity,
        "category": "correctness",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    result = ResponseParser.parse(response)

    assert result.findings[0].severity == severity


def test_parse_normalizes_severity():
    finding = {
        "severity": "HIGH",
        "category": "correctness",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    result = ResponseParser.parse(response)

    assert result.findings[0].severity == "high"


def test_parse_rejects_unsupported_severity():
    finding = {
        "severity": "blocker",
        "category": "correctness",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "category",
    [
        "correctness",
        "security",
        "performance",
        "maintainability",
        "design",
        "testing",
        "style",
    ],
)
def test_parse_accepts_supported_category(category):
    finding = {
        "severity": "medium",
        "category": category,
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    result = ResponseParser.parse(response)

    assert result.findings[0].category == category


def test_parse_normalizes_category():
    finding = {
        "severity": "medium",
        "category": "SECURITY",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    result = ResponseParser.parse(response)

    assert result.findings[0].category == "security"


def test_parse_rejects_unsupported_category():
    finding = {
        "severity": "medium",
        "category": "architecture",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_finding_severity():
    finding = {
        "severity": " ",
        "category": "correctness",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_finding_category():
    finding = {
        "severity": "high",
        "category": " ",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_finding_path():
    finding = {
        "severity": "high",
        "category": "correctness",
        "path": "",
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


@pytest.mark.parametrize(
    "path",
    [
        "/brain/example.py",
        "\\brain\\example.py",
        "../example.py",
        "brain/../example.py",
        "brain\\..\\example.py",
    ],
)
def test_parse_rejects_invalid_finding_path(path):
    finding = {
        "severity": "high",
        "category": "correctness",
        "path": path,
        "message": "Problem.",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_message():
    finding = {
        "severity": "high",
        "category": "correctness",
        "path": "brain/example.py",
        "message": " ",
        "recommendation": "Fix it.",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)


def test_parse_rejects_empty_recommendation():
    finding = {
        "severity": "high",
        "category": "correctness",
        "path": "brain/example.py",
        "message": "Problem.",
        "recommendation": " ",
    }

    response = json.dumps(
        {
            "approved": False,
            "findings": [finding],
            "summary": "Review complete.",
        }
    )

    with pytest.raises(ValueError):
        ResponseParser.parse(response)