from brain.code.models.code_structure import CodeStructure
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task
from brain.engineering.verification.models.verification_request import (
    VerificationRequest,
)


def test_verification_request_can_be_constructed():
    task = Task(
        id="task-1",
        description="Verify implementation",
        category="verification",
        dependencies=frozenset(),
        affected_areas=frozenset({"module"}),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("verify implementation",),
        milestones=("verification",),
        required_capabilities=frozenset(
            {"verification"}
        ),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=("run tests",),
        confidence=1.0,
    )

    existing_code = CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )

    proposed_changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return value",
        ),
    )

    request = VerificationRequest(
        task=task,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
        command="pytest tests/example.py -q",
    )

    assert request.task is task
    assert request.plan is plan
    assert request.existing_code is existing_code
    assert request.proposed_changes == proposed_changes
    assert request.command == "pytest tests/example.py -q"