import json

import pytest

from brain.engineering.requirements.ai_requirement_interpreter import (
    AIRequirementInterpreter,
)


class FakeChatService:

    def __init__(
        self,
        response: str,
    ):
        self._response = response
        self.last_prompt = None

    def chat(
        self,
        prompt: str,
    ) -> str:
        self.last_prompt = prompt
        return self._response

def test_interpreter_includes_request_in_prompt():

    chat_service = FakeChatService(
        valid_response()
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    request = "Build an API for managing books"

    interpreter.interpret(
        request
    )

    assert request in chat_service.last_prompt

def test_interpreter_uses_ai_response_for_requirement_fields():

    response = json.dumps({
        "objective": "Manage library books",
        "functional_requirements": [
            "Create books",
            "Delete books",
        ],
        "non_functional_requirements": [
            "API must be reliable",
        ],
        "constraints": [
            "Use REST",
        ],
        "acceptance_criteria": [
            "Books can be created and deleted",
        ],
        "assumptions": [
            "A database is available",
        ],
        "ambiguities": [
            "Authentication method is unspecified",
        ],
        "affected_areas": [
            "API",
            "database",
        ],
        "confidence": 0.82,
    })

    chat_service = FakeChatService(
        response
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    result = interpreter.interpret(
        "Build something completely different"
    )

    assert result.objective == "Manage library books"
    assert result.functional_requirements == frozenset({
        "Create books",
        "Delete books",
    })
    assert result.non_functional_requirements == frozenset({
        "API must be reliable",
    })
    assert result.constraints == frozenset({
        "Use REST",
    })
    assert result.acceptance_criteria == frozenset({
        "Books can be created and deleted",
    })
    assert result.assumptions == frozenset({
        "A database is available",
    })
    assert result.ambiguities == frozenset({
        "Authentication method is unspecified",
    })
    assert result.affected_areas == frozenset({
        "API",
        "database",
    })
    assert result.confidence == 0.82

def test_interpreter_rejects_invalid_json():

    chat_service = FakeChatService(
        "{invalid json"
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_missing_field():

    data = json.loads(valid_response())

    del data["objective"]

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_extra_field():

    data = json.loads(valid_response())

    data["unexpected_field"] = "not allowed"

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_non_object_json():

    chat_service = FakeChatService(
        json.dumps(["not", "an", "object"])
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_non_string_objective():

    data = json.loads(valid_response())
    data["objective"] = 123

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

@pytest.mark.parametrize(
    "field",
    [
        "functional_requirements",
        "non_functional_requirements",
        "constraints",
        "acceptance_criteria",
        "assumptions",
        "ambiguities",
        "affected_areas",
    ],
)
def test_interpreter_rejects_non_list_requirement_field(
    field,
):

    data = json.loads(valid_response())
    data[field] = "invalid"

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

@pytest.mark.parametrize(
    "field",
    [
        "functional_requirements",
        "non_functional_requirements",
        "constraints",
        "acceptance_criteria",
        "assumptions",
        "ambiguities",
        "affected_areas",
    ],
)
def test_interpreter_rejects_non_string_requirement_item(
    field,
):

    data = json.loads(valid_response())
    data[field] = ["valid", 123]

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_boolean_confidence():

    data = json.loads(valid_response())
    data["confidence"] = True

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_non_numeric_confidence():

    data = json.loads(valid_response())
    data["confidence"] = "high"

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_confidence_below_zero():

    data = json.loads(valid_response())
    data["confidence"] = -0.1

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_confidence_above_one():

    data = json.loads(valid_response())
    data["confidence"] = 1.1

    chat_service = FakeChatService(
        json.dumps(data)
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_empty_ai_response():

    chat_service = FakeChatService(
        ""
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_non_string_ai_response():

    chat_service = FakeChatService(
        None
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_rejects_non_string_request():

    chat_service = FakeChatService(
        valid_response()
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            123
        )

def test_interpreter_rejects_empty_request():

    chat_service = FakeChatService(
        valid_response()
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(ValueError):
        interpreter.interpret(
            "   "
        )

class FakeChatService:

    def __init__(
        self,
        response: str,
    ):
        self._response = response
        self.last_prompt = None
        self.call_count = 0

    def chat(
        self,
        prompt: str,
    ) -> str:
        self.last_prompt = prompt
        self.call_count += 1
        return self._response

def test_interpreter_calls_chat_service_once():

    chat_service = FakeChatService(
        valid_response()
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    interpreter.interpret(
        "Build an API"
    )

    assert chat_service.call_count == 1

def test_interpreter_returns_immutable_requirement_collections():

    chat_service = FakeChatService(
        valid_response()
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    result = interpreter.interpret(
        "Build an API"
    )

    assert isinstance(
        result.functional_requirements,
        frozenset,
    )
    assert isinstance(
        result.non_functional_requirements,
        frozenset,
    )
    assert isinstance(
        result.constraints,
        frozenset,
    )
    assert isinstance(
        result.acceptance_criteria,
        frozenset,
    )
    assert isinstance(
        result.assumptions,
        frozenset,
    )
    assert isinstance(
        result.ambiguities,
        frozenset,
    )
    assert isinstance(
        result.affected_areas,
        frozenset,
    )
def valid_response() -> str:

    return json.dumps({
        "objective": "Add authentication to the application",
        "functional_requirements": [
            "Users can authenticate",
        ],
        "non_functional_requirements": [
            "Authentication must be secure",
        ],
        "constraints": [
            "Use the existing backend",
        ],
        "acceptance_criteria": [
            "Authenticated users can access protected resources",
        ],
        "assumptions": [
            "A user database already exists",
        ],
        "ambiguities": [],
        "affected_areas": [
            "authentication",
            "application backend",
        ],
        "confidence": 0.95,
    })


def test_interpreter_rejects_wrong_field_type():

    data = json.loads(valid_response())

    data["functional_requirements"] = (
        "Users can authenticate"
    )

    response = json.dumps(data)

    chat_service = FakeChatService(
        response
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    with pytest.raises(TypeError):
        interpreter.interpret(
            "Build an API"
        )

def test_interpreter_preserves_original_request():

    response = valid_response()

    chat_service = FakeChatService(
        response
    )

    interpreter = AIRequirementInterpreter(
        chat_service
    )

    request = "Build an API for managing books"

    result = interpreter.interpret(
        request
    )

    assert result.original_request == request