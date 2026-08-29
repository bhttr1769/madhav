import json

import pytest

from brain.engineering.planning.ai_engineering_planner import (
    AIEngineeringPlanner,
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

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
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


def decomposition() -> TaskDecomposition:

    requirement = Requirement(
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

    tasks = (
        Task(
            id="task-1",
            description="Design the API",
            category="design",
            dependencies=frozenset(),
            affected_areas=frozenset({
                "backend",
            }),
            acceptance_criteria=frozenset({
                "API design is defined",
            }),
        ),
        Task(
            id="task-2",
            description="Implement the API",
            category="implementation",
            dependencies=frozenset({
                "task-1",
            }),
            affected_areas=frozenset({
                "backend",
            }),
            acceptance_criteria=frozenset({
                "API endpoints are implemented",
            }),
        ),
        Task(
            id="task-3",
            description="Test the API",
            category="testing",
            dependencies=frozenset({
                "task-2",
            }),
            affected_areas=frozenset({
                "backend",
            }),
            acceptance_criteria=frozenset({
                "API behavior is verified",
            }),
        ),
    )

    return TaskDecomposition(
        requirement=requirement,
        tasks=tasks,
    )


def valid_response() -> str:

    return json.dumps({
        "task_order": [
            "task-1",
            "task-2",
            "task-3",
        ],
        "strategy": [
            "Complete API design before implementation.",
            "Validate implementation through testing.",
        ],
        "milestones": [
            "API design complete",
            "API implementation complete",
            "API validation complete",
        ],
        "required_capabilities": [
            "Python",
            "pytest",
        ],
        "risks": [
            "Implementation may conflict with existing backend behavior",
        ],
        "assumptions": [
            "The existing backend is available",
        ],
        "validation_strategy": [
            "Run the API test suite.",
            "Verify all acceptance criteria.",
        ],
        "confidence": 0.9,
    })


def create_planner(
    response=None,
):

    if response is None:
        response = valid_response()

    chat_service = FakeChatService(
        response
    )

    planner = AIEngineeringPlanner(
        chat_service
    )

    return planner, chat_service


def test_planner_accepts_chat_service():

    planner, _ = create_planner()

    assert isinstance(
        planner,
        AIEngineeringPlanner,
    )


def test_planner_rejects_invalid_chat_service():

    with pytest.raises(TypeError):

        AIEngineeringPlanner(
            object()
        )


def test_planner_rejects_invalid_decomposition():

    planner, _ = create_planner()

    with pytest.raises(TypeError):

        planner.plan(
            object()
        )


def test_planner_calls_chat_service():

    planner, chat_service = create_planner()

    planner.plan(
        decomposition()
    )

    assert chat_service.call_count == 1


def test_planner_sends_decomposition_to_ai():

    planner, chat_service = create_planner()

    planner.plan(
        decomposition()
    )

    assert "Build an API" in chat_service.last_prompt
    assert "task-1" in chat_service.last_prompt
    assert "task-2" in chat_service.last_prompt
    assert "task-3" in chat_service.last_prompt


def test_planner_returns_engineering_plan():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert isinstance(
        result,
        EngineeringPlan,
    )


def test_planner_preserves_task_order():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.task_order == (
        "task-1",
        "task-2",
        "task-3",
    )


def test_planner_preserves_strategy():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.strategy == (
        "Complete API design before implementation.",
        "Validate implementation through testing.",
    )


def test_planner_preserves_milestones():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.milestones == (
        "API design complete",
        "API implementation complete",
        "API validation complete",
    )


def test_planner_preserves_required_capabilities():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.required_capabilities == frozenset({
        "Python",
        "pytest",
    })


def test_planner_preserves_risks():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.risks == frozenset({
        "Implementation may conflict with existing backend behavior",
    })


def test_planner_preserves_assumptions():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.assumptions == frozenset({
        "The existing backend is available",
    })


def test_planner_preserves_validation_strategy():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.validation_strategy == (
        "Run the API test suite.",
        "Verify all acceptance criteria.",
    )


def test_planner_preserves_confidence():

    planner, _ = create_planner()

    result = planner.plan(
        decomposition()
    )

    assert result.confidence == 0.9


def test_planner_rejects_non_string_response():

    planner, _ = create_planner()

    planner._chat_service._response = None

    with pytest.raises(TypeError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_invalid_json():

    planner, _ = create_planner(
        "not json"
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_non_object_json():

    planner, _ = create_planner(
        json.dumps([])
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_invalid_schema():

    response = json.loads(
        valid_response()
    )

    del response["risks"]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


@pytest.mark.parametrize(
    "field",
    [
        "task_order",
        "strategy",
        "milestones",
        "required_capabilities",
        "risks",
        "assumptions",
        "validation_strategy",
    ],
)
def test_planner_rejects_non_list_fields(
    field,
):

    response = json.loads(
        valid_response()
    )

    response[field] = "invalid"

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        planner.plan(
            decomposition()
        )


@pytest.mark.parametrize(
    "field",
    [
        "task_order",
        "strategy",
        "milestones",
        "required_capabilities",
        "risks",
        "assumptions",
        "validation_strategy",
    ],
)
def test_planner_rejects_non_string_list_items(
    field,
):

    response = json.loads(
        valid_response()
    )

    response[field] = [1]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        planner.plan(
            decomposition()
        )


@pytest.mark.parametrize(
    "field",
    [
        "task_order",
        "strategy",
        "milestones",
        "required_capabilities",
        "risks",
        "assumptions",
        "validation_strategy",
    ],
)
def test_planner_rejects_empty_strings_in_lists(
    field,
):

    response = json.loads(
        valid_response()
    )

    if field == "task_order":
        response[field] = [
            "task-1",
            "",
            "task-3",
        ]
    else:
        response[field] = [""]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


@pytest.mark.parametrize(
    "confidence",
    [
        -0.1,
        1.1,
    ],
)
def test_planner_rejects_invalid_confidence(
    confidence,
):

    response = json.loads(
        valid_response()
    )

    response["confidence"] = confidence

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_boolean_confidence():

    response = json.loads(
        valid_response()
    )

    response["confidence"] = True

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(TypeError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_duplicate_task_ids():

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-1",
        "task-2",
        "task-2",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_missing_task():

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-1",
        "task-2",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_unknown_task():

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-1",
        "task-2",
        "task-999",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )


def test_planner_rejects_dependency_order_violation():

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-2",
        "task-1",
        "task-3",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            decomposition()
        )

def branching_decomposition() -> TaskDecomposition:

    requirement = Requirement(
        original_request="Build a service",
        objective="Build a service",
        functional_requirements=frozenset(),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(),
        confidence=1.0,
    )

    tasks = (
        Task(
            id="task-1",
            description="Define the data model",
            category="design",
            dependencies=frozenset(),
            affected_areas=frozenset(),
            acceptance_criteria=frozenset(),
        ),
        Task(
            id="task-2",
            description="Implement the backend",
            category="implementation",
            dependencies=frozenset({"task-1"}),
            affected_areas=frozenset(),
            acceptance_criteria=frozenset(),
        ),
        Task(
            id="task-3",
            description="Implement the API",
            category="implementation",
            dependencies=frozenset({"task-1"}),
            affected_areas=frozenset(),
            acceptance_criteria=frozenset(),
        ),
        Task(
            id="task-4",
            description="Integrate the service",
            category="integration",
            dependencies=frozenset({
                "task-2",
                "task-3",
            }),
            affected_areas=frozenset(),
            acceptance_criteria=frozenset(),
        ),
    )

    return TaskDecomposition(
        requirement=requirement,
        tasks=tasks,
    )


def test_planner_accepts_branching_dependency_graph():

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-1",
        "task-2",
        "task-3",
        "task-4",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    result = planner.plan(
        branching_decomposition()
    )

    assert result.task_order == (
        "task-1",
        "task-2",
        "task-3",
        "task-4",
    )


def test_planner_rejects_branching_dependency_violation():

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-1",
        "task-4",
        "task-2",
        "task-3",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    with pytest.raises(ValueError):

        planner.plan(
            branching_decomposition()
        )


def test_planner_accepts_independent_tasks():

    requirement = Requirement(
        original_request="Perform independent work",
        objective="Perform independent work",
        functional_requirements=frozenset(),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(),
        confidence=1.0,
    )

    tasks = (
        Task(
            id="task-1",
            description="Analyze component A",
            category="analysis",
            dependencies=frozenset(),
            affected_areas=frozenset(),
            acceptance_criteria=frozenset(),
        ),
        Task(
            id="task-2",
            description="Analyze component B",
            category="analysis",
            dependencies=frozenset(),
            affected_areas=frozenset(),
            acceptance_criteria=frozenset(),
        ),
    )

    decomposition = TaskDecomposition(
        requirement=requirement,
        tasks=tasks,
    )

    response = json.loads(
        valid_response()
    )

    response["task_order"] = [
        "task-2",
        "task-1",
    ]

    planner, _ = create_planner(
        json.dumps(response)
    )

    result = planner.plan(
        decomposition
    )

    assert result.task_order == (
        "task-2",
        "task-1",
    )