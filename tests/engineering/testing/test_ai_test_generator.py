import json

import pytest

from brain.code.models.code_structure import CodeStructure
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.tasks.models.task import Task
from brain.engineering.testing.ai_test_generator import (
    AITestGenerator,
)
from brain.engineering.testing.models.test_generation_request import (
    TestGenerationRequest as GenerationRequest,
)

from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult as GenerationResult,
)

class FakeChatService:
    def __init__(self, response: str):
        self.response = response
        self.last_prompt = None
        self.call_count = 0

    def chat(self, prompt: str) -> str:
        self.last_prompt = prompt
        self.call_count += 1
        return self.response


def valid_response() -> str:
    return json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "create",
                    "content": "def test_health():\n    assert True",
                }
            ]
        }
    )


@pytest.fixture
def requirement():
    return Requirement(
        original_request="Add health checking",
        objective="Provide health checking",
        functional_requirements=frozenset(
            {"health endpoint"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"health check returns success"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({"health"}),
        confidence=1.0,
    )


@pytest.fixture
def task():
    return Task(
        id="task-1",
        description="Implement health checking",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({"health"}),
        acceptance_criteria=frozenset(
            {"health check returns success"}
        ),
    )


@pytest.fixture
def design(requirement, task):
    return SystemDesign(
        requirement=requirement,
        tasks=(task,),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(
            {"health check returns success"}
        ),
    )


@pytest.fixture
def plan():
    return EngineeringPlan(
        task_order=("task-1",),
        strategy=("implement health checking",),
        milestones=("health checking complete",),
        required_capabilities=frozenset({"health checking"}),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=("run tests",),
        confidence=1.0,
    )


@pytest.fixture
def existing_code():
    return CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )


@pytest.fixture
def proposed_changes():
    return (
        CodeChange(
            path="brain/health.py",
            operation="create",
            content="def health():\n    return True",
        ),
    )


@pytest.fixture
def generation_request(
    task,
    design,
    plan,
    existing_code,
    proposed_changes,
):
    return GenerationRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
    )


def test_requires_chat_service():
    with pytest.raises(TypeError):
        AITestGenerator(object())


def test_accepts_chat_service():
    generator = AITestGenerator(
        FakeChatService(valid_response())
    )

    assert generator is not None


def test_rejects_invalid_request():
    generator = AITestGenerator(
        FakeChatService(valid_response())
    )

    with pytest.raises(TypeError):
        generator.generate(object())


def test_calls_chat_service(
    generation_request,
):
    chat_service = FakeChatService(valid_response())
    generator = AITestGenerator(chat_service)

    generator.generate(generation_request)

    assert chat_service.call_count == 1


def test_prompt_contains_task(
    generation_request,
):
    chat_service = FakeChatService(valid_response())
    generator = AITestGenerator(chat_service)

    generator.generate(generation_request)

    assert generation_request.task.id in chat_service.last_prompt
    assert (
        generation_request.task.description
        in chat_service.last_prompt
    )


def test_prompt_contains_acceptance_criteria(
    generation_request,
):
    chat_service = FakeChatService(valid_response())
    generator = AITestGenerator(chat_service)

    generator.generate(generation_request)

    assert (
        "health check returns success"
        in chat_service.last_prompt
    )


def test_prompt_contains_proposed_changes(
    generation_request,
):
    chat_service = FakeChatService(valid_response())
    generator = AITestGenerator(chat_service)

    generator.generate(generation_request)

    assert "brain/health.py" in chat_service.last_prompt
    assert "def health()" in chat_service.last_prompt


def test_prompt_requires_json(
    generation_request,
):
    chat_service = FakeChatService(valid_response())
    generator = AITestGenerator(chat_service)

    generator.generate(generation_request)

    assert "Return ONLY valid JSON." in chat_service.last_prompt


def test_returns_test_generation_result(
    generation_request,
):
    generator = AITestGenerator(
        FakeChatService(valid_response())
    )

    result = generator.generate(generation_request)

    assert isinstance(result, GenerationResult)


def test_preserves_generated_changes(
    generation_request,
):
    generator = AITestGenerator(
        FakeChatService(valid_response())
    )

    result = generator.generate(generation_request)

    assert len(result.changes) == 1

    change = result.changes[0]

    assert change.path == "tests/test_health.py"
    assert change.operation == "create"
    assert change.content == (
        "def test_health():\n    assert True"
    )


def test_propagates_invalid_ai_response(
    generation_request,
):
    generator = AITestGenerator(
        FakeChatService("{invalid")
    )

    with pytest.raises(ValueError):
        generator.generate(generation_request)


def test_propagates_invalid_response_schema(
    generation_request,
):
    generator = AITestGenerator(
        FakeChatService(
            json.dumps(
                {
                    "changes": [],
                    "decision": {},
                }
            )
        )
    )

    with pytest.raises(ValueError):
        generator.generate(generation_request)


def test_supports_empty_generation_result(
    generation_request,
):
    generator = AITestGenerator(
        FakeChatService(
            json.dumps({"changes": []})
        )
    )

    result = generator.generate(generation_request)

    assert result.changes == ()

def test_generator_passes_ai_response_to_parser(
    generation_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "tests/test_health.py",
                    "operation": "create",
                    "content": "def test_health():\n    assert True",
                },
                {
                    "path": "tests/test_health_error.py",
                    "operation": "create",
                    "content": "def test_health_error():\n    assert True",
                },
            ]
        }
    )

    chat_service = FakeChatService(response)
    generator = AITestGenerator(chat_service)

    result = generator.generate(generation_request)

    assert len(result.changes) == 2
    assert result.changes[0].path == "tests/test_health.py"
    assert result.changes[1].path == "tests/test_health_error.py"


def test_generator_preserves_empty_changes_from_ai(
    generation_request,
):
    chat_service = FakeChatService(
        json.dumps({"changes": []})
    )

    generator = AITestGenerator(chat_service)

    result = generator.generate(generation_request)

    assert result.changes == ()


def test_generator_rejects_invalid_change_from_ai(
    generation_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "../unsafe_test.py",
                    "operation": "create",
                    "content": "test",
                }
            ]
        }
    )

    generator = AITestGenerator(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        generator.generate(generation_request)


def test_generator_sends_complete_engineering_context(
    generation_request,
):
    chat_service = FakeChatService(valid_response())
    generator = AITestGenerator(chat_service)

    generator.generate(generation_request)

    prompt = chat_service.last_prompt

    assert generation_request.task.id in prompt
    assert generation_request.design.requirement.objective in prompt
    assert generation_request.plan.task_order[0] in prompt

    proposed_change = generation_request.proposed_changes[0]

    assert proposed_change.path in prompt
    assert proposed_change.operation in prompt
    assert repr(proposed_change.content) in prompt


def test_generator_does_not_require_engineering_decision(
    generation_request,
):
    assert not hasattr(
        generation_request,
        "engineering_decision",
    )

    generator = AITestGenerator(
        FakeChatService(valid_response())
    )

    result = generator.generate(generation_request)

    assert isinstance(result, GenerationResult)