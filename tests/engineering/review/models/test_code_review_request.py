import pytest

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.review.models.code_review_request import (
    CodeReviewRequest,
)
from brain.engineering.tasks.models.task import Task


@pytest.fixture
def requirement():
    return Requirement(
        original_request="Add a feature",
        objective="Provide the requested feature",
        functional_requirements=frozenset(
            {"feature behavior"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"feature works"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({"feature"}),
        confidence=1.0,
    )


@pytest.fixture
def task():
    return Task(
        id="task-1",
        description="Implement feature",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({"feature"}),
        acceptance_criteria=frozenset(
            {"feature works"}
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
            {"feature works"}
        ),
    )


@pytest.fixture
def plan():
    return EngineeringPlan(
        task_order=("task-1",),
        strategy=("implement feature",),
        milestones=("feature complete",),
        required_capabilities=frozenset(),
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
            path="brain/example.py",
            operation="create",
            content="def example():\n    return True",
        ),
    )


def test_code_review_request_is_constructible(
    task,
    design,
    plan,
    existing_code,
    proposed_changes,
):
    request = CodeReviewRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
    )

    assert request.task is task
    assert request.design is design
    assert request.plan is plan
    assert request.existing_code is existing_code
    assert request.proposed_changes == proposed_changes