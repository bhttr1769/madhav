from brain.engineering.planning.fake_planner import (
    FakePlanner,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.planning.planner import (
    Planner,
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


def decomposition() -> TaskDecomposition:

    requirement = Requirement(
        original_request="Build an API",
        objective="Build an API",
        functional_requirements=frozenset({
            "The API must expose endpoints",
        }),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=1.0,
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
            acceptance_criteria=frozenset(),
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
            acceptance_criteria=frozenset(),
        ),
    )

    return TaskDecomposition(
        requirement=requirement,
        tasks=tasks,
    )


def plan() -> EngineeringPlan:

    return EngineeringPlan(
        task_order=(
            "task-1",
            "task-2",
        ),
        strategy=(
            "Design before implementation.",
        ),
        milestones=(
            "API design complete",
            "API implementation complete",
        ),
        required_capabilities=frozenset({
            "Python",
        }),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=(
            "Run the test suite.",
        ),
        confidence=0.9,
    )


def test_planner_is_interface():

    assert Planner.__abstractmethods__ == {
        "plan",
    }


def test_fake_planner_returns_result():

    planner = FakePlanner(
        result=plan(),
    )

    result = planner.plan(
        decomposition(),
    )

    assert result == plan()