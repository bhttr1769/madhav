from brain.code.models.code_structure import CodeStructure
from brain.engineering.debugging.models.debugging_request import (
    DebuggingRequest,
)
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task


def test_debugging_request_can_be_constructed():
    task = Task(
        id="task-1",
        description="Fix failing implementation",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({"module"}),
        acceptance_criteria=frozenset({"error is resolved"}),
    )

    design = SystemDesign(
        requirement=None,
        tasks=(task,),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("fix the defect",),
        milestones=("implementation",),
        required_capabilities=frozenset({"debugging"}),
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

    request = DebuggingRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
        error_message="NameError: name 'value' is not defined",
        traceback="Traceback ...",
    )

    assert request.task is task
    assert request.design is design
    assert request.plan is plan
    assert request.existing_code is existing_code
    assert request.proposed_changes == proposed_changes
    assert request.error_message == (
        "NameError: name 'value' is not defined"
    )
    assert request.traceback == "Traceback ..."