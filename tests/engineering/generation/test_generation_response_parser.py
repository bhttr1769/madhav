
import json

import pytest

from brain.engineering.generation.generation_response_parser import (
    GenerationResponseParser,
)
from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)
from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


def valid_response():
    return json.dumps({
        "changes": [
            {
                "path": "backend/health.py",
                "operation": "create",
                "content": (
                    "def health():\n"
                    "    return {'status': 'ok'}\n"
                ),
            },
        ],
        "decision": {
            "implementation_required": True,
            "necessity": (
                "A new implementation is required "
                "to satisfy the health endpoint task."
            ),
            "reuse_existing": True,
            "use_standard_library": True,
            "use_existing_dependency": False,
            "new_dependency_required": False,
            "abstraction_justified": False,
            "optimization_justified": False,
            "rationale": [
                "The existing backend should be reused.",
                "No new dependency is required.",
            ],
        },
    })


def test_parser_returns_generation_result():

    result = GenerationResponseParser.parse(
        valid_response(),
    )

    assert isinstance(
        result,
        GenerationResult,
    )


def test_parser_preserves_code_changes():

    result = GenerationResponseParser.parse(
        valid_response(),
    )

    assert result.changes == (
        CodeChange(
            path="backend/health.py",
            operation="create",
            content=(
                "def health():\n"
                "    return {'status': 'ok'}\n"
            ),
        ),
    )


def test_parser_preserves_engineering_decision():

    result = GenerationResponseParser.parse(
        valid_response(),
    )

    assert result.decision == EngineeringDecision(
        implementation_required=True,
        necessity=(
            "A new implementation is required "
            "to satisfy the health endpoint task."
        ),
        reuse_existing=True,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "The existing backend should be reused.",
            "No new dependency is required.",
        ),
    )


def test_parser_rejects_non_string_response():

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            object(),
        )


def test_parser_rejects_invalid_json():

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            "not json",
        )


def test_parser_rejects_non_object_response():

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps([]),
        )


def test_parser_rejects_invalid_top_level_schema():

    data = json.loads(
        valid_response(),
    )

    data["extra"] = "value"

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_list_changes():

    data = json.loads(
        valid_response(),
    )

    data["changes"] = {}

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_object_change():

    data = json.loads(
        valid_response(),
    )

    data["changes"] = ["invalid"]

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_invalid_change_schema():

    data = json.loads(
        valid_response(),
    )

    del data["changes"][0]["content"]

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_string_change_field():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["path"] = 123

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_empty_change_field():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["path"] = " "

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_unsupported_operation():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["operation"] = "execute"

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_absolute_path():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["path"] = "/outside.py"

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_parent_traversal():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["path"] = "../outside.py"

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_duplicate_paths():

    data = json.loads(
        valid_response(),
    )

    data["changes"].append({
        "path": "backend/health.py",
        "operation": "modify",
        "content": "updated",
    })

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_empty_create_content():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["content"] = ""

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_empty_delete_content():

    data = json.loads(
        valid_response(),
    )

    data["changes"][0]["operation"] = "delete"
    data["changes"][0]["content"] = ""

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_object_decision():

    data = json.loads(
        valid_response(),
    )

    data["decision"] = []

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_invalid_decision_schema():

    data = json.loads(
        valid_response(),
    )

    del data["decision"]["necessity"]

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_string_necessity():

    data = json.loads(
        valid_response(),
    )

    data["decision"]["necessity"] = 123

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_empty_necessity():

    data = json.loads(
        valid_response(),
    )

    data["decision"]["necessity"] = " "

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


@pytest.mark.parametrize(
    "field",
    [
        "implementation_required",
        "reuse_existing",
        "use_standard_library",
        "use_existing_dependency",
        "new_dependency_required",
        "abstraction_justified",
        "optimization_justified",
    ],
)
def test_parser_rejects_non_boolean_decision_field(
    field,
):

    data = json.loads(
        valid_response(),
    )

    data["decision"][field] = "true"

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_list_rationale():

    data = json.loads(
        valid_response(),
    )

    data["decision"]["rationale"] = "invalid"

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_non_string_rationale_item():

    data = json.loads(
        valid_response(),
    )

    data["decision"]["rationale"] = [123]

    with pytest.raises(TypeError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )


def test_parser_rejects_empty_rationale_item():

    data = json.loads(
        valid_response(),
    )

    data["decision"]["rationale"] = [" "]

    with pytest.raises(ValueError):

        GenerationResponseParser.parse(
            json.dumps(data),
        )