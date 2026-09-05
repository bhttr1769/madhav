
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

from brain.engineering.design.models.data_flow import (
    DataFlow,
)

from brain.engineering.design.models.design_component import (
    DesignComponent,
)

from brain.engineering.design.models.design_dependency import (
    DesignDependency,
)

from brain.engineering.design.models.design_interface import (
    DesignInterface,
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


def requirement() -> Requirement:

    return Requirement(
        original_request="Build an API",
        objective="Build an API",
        functional_requirements=frozenset({
            "The API must expose endpoints",
        }),
        non_functional_requirements=frozenset({
            "The API must be reliable",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "API endpoints respond correctly",
        }),
        assumptions=frozenset({
            "The existing backend is available",
        }),
        ambiguities=frozenset({
            "Authentication mechanism is unspecified",
        }),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=0.9,
    )


def task() -> Task:

    return Task(
        id="task-1",
        description="Implement the API",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        acceptance_criteria=frozenset({
            "API endpoints are implemented",
        }),
    )


def design() -> SystemDesign:

    return SystemDesign(
        requirement=requirement(),
        tasks=(task(),),
        components=(
            DesignComponent(
                id="api",
                name="API",
                responsibility="Expose API endpoints",
                layer="application",
                interfaces=frozenset({
                    "api-interface",
                }),
            ),
        ),
        interfaces=(
            DesignInterface(
                id="api-interface",
                name="API Interface",
                owner="api",
                consumers=frozenset(),
                purpose="Expose API operations",
            ),
        ),
        dependencies=(),
        data_flows=(),
        constraints=frozenset({
            "Use the existing backend",
        }),
        decisions=frozenset({
            "Reuse the existing backend",
        }),
        acceptance_criteria=frozenset({
            "API endpoints respond correctly",
        }),
    )


def plan() -> EngineeringPlan:

    return EngineeringPlan(
        task_order=("task-1",),
        strategy=(
            "Implement the API using the existing backend.",
        ),
        milestones=(
            "API implementation complete",
        ),
        required_capabilities=frozenset({
            "Python",
        }),
        risks=frozenset({
            "Implementation may conflict with existing backend behavior",
        }),
        assumptions=frozenset({
            "The existing backend is available",
        }),
        validation_strategy=(
            "Run the API test suite.",
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
                "path": "api.py",
                "operation": "create",
                "content": "def handle_request():\n    pass\n",
            },
        ],
        "decision": {
            "implementation_required": True,
            "necessity": "Implementation is required to satisfy the task.",
            "reuse_existing": True,
            "use_standard_library": True,
            "use_existing_dependency": False,
            "new_dependency_required": False,
            "abstraction_justified": False,
            "optimization_justified": False,
            "rationale": [
                "The task requires concrete API implementation.",
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
        response
    )

    generator = AICodeGenerator(
        chat_service
    )

    return generator, chat_service


def test_generator_accepts_chat_service():

    generator, _ = create_generator()

    assert isinstance(
        generator,
        AICodeGenerator,
    )


def test_generator_rejects_invalid_chat_service():

    with pytest.raises(TypeError):

        AICodeGenerator(
            object()
        )


def test_generator_rejects_invalid_request():

    generator, _ = create_generator()

    with pytest.raises(TypeError):

        generator.generate(
            object()
        )


def test_generator_calls_chat_service():

    generator, chat_service = create_generator()

    generator.generate(
        generation_request()
    )

    assert chat_service.call_count == 1


def test_generator_sends_task_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        generation_request()
    )

    assert "task-1" in chat_service.last_prompt
    assert "Implement the API" in chat_service.last_prompt


def test_generator_sends_design_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        generation_request()
    )

    assert "API Interface" in chat_service.last_prompt
    assert "Expose API endpoints" in chat_service.last_prompt


def test_generator_sends_plan_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        generation_request()
    )

    assert "Implement the API using the existing backend." in (
        chat_service.last_prompt
    )
    assert "API implementation complete" in (
        chat_service.last_prompt
    )


def test_generator_returns_generation_result():

    generator, _ = create_generator()

    result = generator.generate(
        generation_request()
    )

    assert isinstance(
        result,
        GenerationResult,
    )


def test_generator_preserves_changes():

    generator, _ = create_generator()

    result = generator.generate(
        generation_request()
    )

    assert result.changes == (
        CodeChange(
            path="api.py",
            operation="create",
            content="def handle_request():\n    pass\n",
        ),
    )


def test_generator_preserves_decision():

    generator, _ = create_generator()

    result = generator.generate(
        generation_request()
    )

    assert result.decision == EngineeringDecision(
        implementation_required=True,
        necessity="Implementation is required to satisfy the task.",
        reuse_existing=True,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "The task requires concrete API implementation.",
            "The existing backend should be reused.",
            "No new dependency is required.",
        ),
    )


def test_generator_rejects_non_string_response():

    generator, _ = create_generator()

    generator._chat_service._response = None

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_invalid_json():

    generator, _ = create_generator(
        "not json"
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_non_object_json():

    generator, _ = create_generator(
        json.dumps([])
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_invalid_top_level_schema():

    response = json.loads(
        valid_response()
    )

    del response["decision"]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_non_list_changes():

    response = json.loads(
        valid_response()
    )

    response["changes"] = "invalid"

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_invalid_change_object():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        "invalid",
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_invalid_change_schema():

    response = json.loads(
        valid_response()
    )

    del response["changes"][0]["content"]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


@pytest.mark.parametrize(
    "field",
    [
        "path",
        "operation",
        "content",
    ],
)
def test_generator_rejects_non_string_change_fields(
    field,
):

    response = json.loads(
        valid_response()
    )

    response["changes"][0][field] = 123

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


@pytest.mark.parametrize(
    "field",
    [
        "path",
        "operation",
        "content",
    ],
)
def test_generator_rejects_empty_change_fields(
    field,
):

    response = json.loads(
        valid_response()
    )

    response["changes"][0][field] = "   "

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_accepts_empty_changes():

    response = json.loads(
        valid_response()
    )

    response["changes"] = []

    generator, _ = create_generator(
        json.dumps(response)
    )

    result = generator.generate(
        generation_request()
    )

    assert result.changes == ()


def test_generator_rejects_non_object_decision():

    response = json.loads(
        valid_response()
    )

    response["decision"] = "invalid"

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_invalid_decision_schema():

    response = json.loads(
        valid_response()
    )

    del response["decision"]["necessity"]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_non_string_necessity():

    response = json.loads(
        valid_response()
    )

    response["decision"]["necessity"] = 123

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_empty_necessity():

    response = json.loads(
        valid_response()
    )

    response["decision"]["necessity"] = "   "

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
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
def test_generator_rejects_non_boolean_decision_fields(
    field,
):

    response = json.loads(
        valid_response()
    )

    response["decision"][field] = "true"

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_non_list_rationale():

    response = json.loads(
        valid_response()
    )

    response["decision"]["rationale"] = "invalid"

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_non_string_rationale_items():

    response = json.loads(
        valid_response()
    )

    response["decision"]["rationale"] = [123]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_empty_rationale_items():

    response = json.loads(
        valid_response()
    )

    response["decision"]["rationale"] = [""]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_preserves_multiple_changes():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "api.py",
            "operation": "create",
            "content": "api",
        },
        {
            "path": "tests/test_api.py",
            "operation": "create",
            "content": "tests",
        },
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    result = generator.generate(
        generation_request()
    )

    assert result.changes == (
        CodeChange(
            path="api.py",
            operation="create",
            content="api",
        ),
        CodeChange(
            path="tests/test_api.py",
            operation="create",
            content="tests",
        ),
    )


def test_generator_preserves_false_decision_flags():

    response = json.loads(
        valid_response()
    )

    response["decision"] = {
        "implementation_required": False,
        "necessity": "No implementation is required.",
        "reuse_existing": False,
        "use_standard_library": False,
        "use_existing_dependency": False,
        "new_dependency_required": False,
        "abstraction_justified": False,
        "optimization_justified": False,
        "rationale": [
            "The existing implementation already satisfies the task.",
        ],
    }

    generator, _ = create_generator(
        json.dumps(response)
    )

    result = generator.generate(
        generation_request()
    )

    assert result.decision == EngineeringDecision(
        implementation_required=False,
        necessity="No implementation is required.",
        reuse_existing=False,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "The existing implementation already satisfies the task.",
        ),
    )


def test_generator_accepts_create_operation():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/example.py",
            "operation": "create",
            "content": "print('hello')",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    result = generator.generate(
        generation_request()
    )

    assert result.changes[0].operation == "create"


def test_generator_accepts_modify_operation():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/example.py",
            "operation": "modify",
            "content": "print('updated')",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    result = generator.generate(
        generation_request()
    )

    assert result.changes[0].operation == "modify"


def test_generator_accepts_delete_operation():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/example.py",
            "operation": "delete",
            "content": "deleted",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    result = generator.generate(
        generation_request()
    )

    assert result.changes[0].operation == "delete"


def test_generator_rejects_unsupported_operation():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/example.py",
            "operation": "rename",
            "content": "example",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_absolute_unix_path():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "/etc/example.py",
            "operation": "modify",
            "content": "example",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_absolute_windows_path():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "\\etc\\example.py",
            "operation": "modify",
            "content": "example",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_parent_path_traversal():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/../example.py",
            "operation": "modify",
            "content": "example",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_duplicate_change_paths():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
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
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_empty_content_for_create():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/example.py",
            "operation": "create",
            "content": "   ",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )


def test_generator_rejects_empty_content_for_modify():

    response = json.loads(
        valid_response()
    )

    response["changes"] = [
        {
            "path": "brain/example.py",
            "operation": "modify",
            "content": "",
        }
    ]

    generator, _ = create_generator(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        generator.generate(
            generation_request()
        )