import pytest

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.tasks.models.task import (
    Task,
)


@pytest.fixture
def task_decomposition() -> TaskDecomposition:

    requirement = Requirement(
        original_request="Build an authentication API",
        objective="Add authentication to the application",
        functional_requirements=frozenset({
            "Users can authenticate",
        }),
        non_functional_requirements=frozenset({
            "Authentication must be secure",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "Authenticated users can access protected resources",
        }),
        assumptions=frozenset({
            "A user database already exists",
        }),
        ambiguities=frozenset({
            "Authentication method is unspecified",
        }),
        affected_areas=frozenset({
            "authentication",
            "application backend",
        }),
        confidence=0.95,
    )

    task = Task(
        id="task-1",
        description="Implement authentication",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "authentication",
        }),
        acceptance_criteria=frozenset({
            "Users can authenticate",
        }),
    )

    return TaskDecomposition(
        requirement=requirement,
        tasks=(task,),
    )

@pytest.fixture
def task(task_decomposition) -> Task:

    return task_decomposition.tasks[0]


@pytest.fixture
def design(task_decomposition) -> SystemDesign:

    return SystemDesign(
        requirement=task_decomposition.requirement,
        tasks=task_decomposition.tasks,
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset({
            "Use the existing backend",
        }),
        decisions=frozenset(),
        acceptance_criteria=frozenset({
            "Users can authenticate",
        }),
    )


@pytest.fixture
def plan() -> EngineeringPlan:

    return EngineeringPlan(
        task_order=("task-1",),
        strategy=(
            "Implement authentication using the existing backend.",
        ),
        milestones=(
            "Authentication implementation complete",
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


@pytest.fixture
def existing_code() -> CodeStructure:

    return CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )