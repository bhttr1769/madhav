import pytest

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)


def valid_plan() -> EngineeringPlan:

    return EngineeringPlan(
        task_order=(
            "task-1",
            "task-2",
        ),
        strategy=(
            "Implement the core functionality first.",
            "Validate integration after implementation.",
        ),
        milestones=(
            "Core implementation complete",
            "Integration validated",
        ),
        required_capabilities=frozenset({
            "Python",
            "pytest",
        }),
        risks=frozenset({
            "Integration failure",
        }),
        assumptions=frozenset({
            "Existing project structure remains compatible",
        }),
        validation_strategy=(
            "Run the complete test suite.",
            "Verify all acceptance criteria.",
        ),
        confidence=0.9,
    )


def test_engineering_plan_is_frozen():

    plan = valid_plan()

    with pytest.raises(AttributeError):
        plan.confidence = 0.5


def test_engineering_plan_stores_task_order():

    plan = valid_plan()

    assert plan.task_order == (
        "task-1",
        "task-2",
    )


def test_engineering_plan_stores_strategy():

    plan = valid_plan()

    assert plan.strategy == (
        "Implement the core functionality first.",
        "Validate integration after implementation.",
    )


def test_engineering_plan_stores_milestones():

    plan = valid_plan()

    assert plan.milestones == (
        "Core implementation complete",
        "Integration validated",
    )


def test_engineering_plan_stores_required_capabilities():

    plan = valid_plan()

    assert plan.required_capabilities == frozenset({
        "Python",
        "pytest",
    })


def test_engineering_plan_stores_risks():

    plan = valid_plan()

    assert plan.risks == frozenset({
        "Integration failure",
    })


def test_engineering_plan_stores_assumptions():

    plan = valid_plan()

    assert plan.assumptions == frozenset({
        "Existing project structure remains compatible",
    })


def test_engineering_plan_stores_validation_strategy():

    plan = valid_plan()

    assert plan.validation_strategy == (
        "Run the complete test suite.",
        "Verify all acceptance criteria.",
    )


def test_engineering_plan_stores_confidence():

    plan = valid_plan()

    assert plan.confidence == 0.9