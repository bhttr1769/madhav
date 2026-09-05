import json

import pytest

from brain.engineering.generation.ai_code_generator import (
    AICodeGenerator,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.generation_request import (
    GenerationRequest,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)

from brain.engineering.generation.code_generator import (
    CodeGenerator,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)


class FakeChatService:

    def __init__(
        self,
        response: str,
    ):
        self.response = response
        self.call_count = 0
        self.last_prompt = None

    def chat(
        self,
        prompt: str,
    ) -> str:

        self.call_count += 1
        self.last_prompt = prompt

        return self.response


def requirement() -> Requirement:

    return Requirement(
        original_request="Add a health endpoint",
        objective="Add a health endpoint",
        functional_requirements=frozenset({
            "Expose a health endpoint",
        }),
        non_functional_requirements=frozenset({
            "The endpoint should be reliable",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "Health endpoint returns successfully",
        }),
        assumptions=frozenset({
            "The existing backend is available",
        }),
        ambiguities=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=0.95,
    )


def task() -> Task:

    return Task(
        id="task-health",
        description="Implement the health endpoint",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        acceptance_criteria=frozenset({
            "Health endpoint returns successfully",
        }),
    )


def design() -> SystemDesign:

    return SystemDesign(
        requirement=requirement(),
        tasks=(task(),),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset({
            "Use the existing backend",
        }),
        decisions=frozenset(),
        acceptance_criteria=frozenset({
            "Health endpoint returns successfully",
        }),
    )


def plan() -> EngineeringPlan:

    return EngineeringPlan(
        task_order=("task-health",),
        strategy=(
            "Implement the endpoint in the existing backend.",
        ),
        milestones=(
            "Health endpoint implemented",
        ),
        required_capabilities=frozenset({
            "Python",
        }),
        risks=frozenset({
            "Implementation may affect existing backend behavior",
        }),
        assumptions=frozenset({
            "The existing backend is available",
        }),
        validation_strategy=(
            "Run the backend test suite.",
        ),
        confidence=0.9,
    )


def generation_request() -> GenerationRequest:

    return GenerationRequest(
        task=task(),
        design=design(),
        plan=plan(),
    )


def valid_response() -> str:

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


def create_generator(
    response=None,
):

    if response is None:
        response = valid_response()

    chat_service = FakeChatService(
        response,
    )

    generator = AICodeGenerator(
        chat_service,
    )

    return generator, chat_service


def test_generation_pipeline_produces_result():

    generator, _ = create_generator()

    result = generator.generate(
        generation_request(),
    )

    assert isinstance(
        result,
        GenerationResult,
    )


def test_generation_pipeline_preserves_code_change():

    generator, _ = create_generator()

    result = generator.generate(
        generation_request(),
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


def test_generation_pipeline_preserves_engineering_decision():

    generator, _ = create_generator()

    result = generator.generate(
        generation_request(),
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


def test_generation_pipeline_sends_context_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        generation_request(),
    )

    assert chat_service.call_count == 1

    assert "task-health" in chat_service.last_prompt
    assert "Implement the health endpoint" in chat_service.last_prompt
    assert "Health endpoint returns successfully" in (
        chat_service.last_prompt
    )


def test_generation_pipeline_rejects_invalid_request():

    generator, _ = create_generator()

    with pytest.raises(TypeError):

        generator.generate(
            object(),
        )


def test_generation_pipeline_rejects_invalid_json():

    generator, _ = create_generator(
        "not json",
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request(),
        )


def test_generation_pipeline_rejects_invalid_change_operation():

    response = json.loads(
        valid_response(),
    )

    response["changes"][0]["operation"] = "execute"

    generator, _ = create_generator(
        json.dumps(response),
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request(),
        )


def test_generation_pipeline_rejects_unsafe_path():

    response = json.loads(
        valid_response(),
    )

    response["changes"][0]["path"] = "../outside.py"

    generator, _ = create_generator(
        json.dumps(response),
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request(),
        )


def test_generation_pipeline_rejects_duplicate_paths():

    response = json.loads(
        valid_response(),
    )

    response["changes"].append({
        "path": "backend/health.py",
        "operation": "modify",
        "content": "updated",
    })

    generator, _ = create_generator(
        json.dumps(response),
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request(),
        )


def test_generation_pipeline_rejects_empty_create_content():

    response = json.loads(
        valid_response(),
    )

    response["changes"][0]["content"] = ""

    generator, _ = create_generator(
        json.dumps(response),
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request(),
        )

