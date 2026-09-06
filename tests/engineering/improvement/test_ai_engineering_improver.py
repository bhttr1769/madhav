import json

import pytest

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.improvement.ai_engineering_improver import (
    AIEngineeringImprover,
)
from brain.engineering.improvement.models.engineering_improvement_request import (
    EngineeringImprovementRequest,
)
from brain.engineering.improvement.models.engineering_improvement_result import (
    EngineeringImprovementResult,
)
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.tasks.models.task import Task


class FakeChatService:
    def __init__(self, response):
        self.response = response
        self.last_prompt = None

    def chat(self, prompt):
        self.last_prompt = prompt
        return self.response


def valid_response():
    return json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": "return value",
                }
            ],
            "rationale": [
                "The implementation can be simplified.",
                "The resulting structure is easier to maintain.",
            ],
        }
    )


@pytest.fixture
def improvement_request():
    requirement = Requirement(
        original_request="Improve the implementation.",
        objective="Improve engineering quality safely.",
        functional_requirements=frozenset(
            {"existing behavior must be preserved"}
        ),
        non_functional_requirements=frozenset(
            {"improve maintainability"}
        ),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"existing behavior remains correct"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(
            {"brain/example.py"}
        ),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Improve implementation",
        category="improvement",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/example.py"}
        ),
        acceptance_criteria=frozenset(
            {"implementation quality is improved"}
        ),
    )

    design = SystemDesign(
        requirement=requirement,
        tasks=(task,),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(
            {"existing behavior remains correct"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("improve implementation safely",),
        milestones=("improvement",),
        required_capabilities=frozenset(
            {"testing", "review", "refactoring"}
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

    return EngineeringImprovementRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
    )


def test_improver_returns_parsed_result(
    improvement_request,
):
    improver = AIEngineeringImprover(
        FakeChatService(valid_response())
    )

    result = improver.improve(
        improvement_request
    )

    assert isinstance(
        result,
        EngineeringImprovementResult,
    )
    assert len(result.changes) == 1
    assert result.changes[0].path == (
        "brain/example.py"
    )
    assert result.changes[0].operation == "modify"
    assert result.rationale == (
        "The implementation can be simplified.",
        "The resulting structure is easier to maintain.",
    )


def test_improver_calls_chat_service(
    improvement_request,
):
    chat_service = FakeChatService(
        valid_response()
    )

    improver = AIEngineeringImprover(
        chat_service
    )

    improver.improve(
        improvement_request
    )

    assert chat_service.last_prompt is not None
    assert chat_service.last_prompt.strip()


def test_improver_rejects_invalid_request():
    improver = AIEngineeringImprover(
        FakeChatService(valid_response())
    )

    with pytest.raises(TypeError):
        improver.improve(None)


def test_improver_rejects_invalid_ai_response(
    improvement_request,
):
    improver = AIEngineeringImprover(
        FakeChatService("not valid json")
    )

    with pytest.raises(ValueError):
        improver.improve(
            improvement_request
        )


def test_improver_handles_no_improvement_required(
    improvement_request,
):
    response = json.dumps(
        {
            "changes": [],
            "rationale": [
                "The implementation is already sufficiently "
                "simple and no improvement is justified."
            ],
        }
    )

    improver = AIEngineeringImprover(
        FakeChatService(response)
    )

    result = improver.improve(
        improvement_request
    )

    assert result.changes == ()
    assert result.rationale == (
        "The implementation is already sufficiently "
        "simple and no improvement is justified.",
    )


def test_improver_sends_complete_engineering_context(
    improvement_request,
):
    chat_service = FakeChatService(
        valid_response()
    )

    improver = AIEngineeringImprover(
        chat_service
    )

    improver.improve(
        improvement_request
    )

    prompt = chat_service.last_prompt

    assert improvement_request.task.id in prompt
    assert (
        improvement_request.design.requirement.objective
        in prompt
    )
    assert (
        improvement_request.plan.task_order[0]
        in prompt
    )

    proposed_change = (
        improvement_request.proposed_changes[0]
    )

    assert proposed_change.path in prompt
    assert proposed_change.operation in prompt
    assert repr(proposed_change.content) in prompt


def test_improver_preserves_parser_validation_boundary(
    improvement_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "../unsafe.py",
                    "operation": "modify",
                    "content": "unsafe",
                }
            ],
            "rationale": [
                "Invalid improvement."
            ],
        }
    )

    improver = AIEngineeringImprover(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        improver.improve(
            improvement_request
        )


def test_improver_does_not_modify_request(
    improvement_request,
):
    original_changes = (
        improvement_request.proposed_changes
    )

    improver = AIEngineeringImprover(
        FakeChatService(valid_response())
    )

    improver.improve(
        improvement_request
    )

    assert (
        improvement_request.proposed_changes
        == original_changes
    )

def test_improver_preserves_multiple_rationales_and_changes(
    improvement_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": (
                        "def example(value):\n"
                        "    return value\n"
                    ),
                },
                {
                    "path": "brain/helper.py",
                    "operation": "create",
                    "content": (
                        "def helper(value):\n"
                        "    return value\n"
                    ),
                },
            ],
            "rationale": [
                "Repeated logic was extracted.",
                "The resulting structure is easier to maintain.",
            ],
        }
    )

    improver = AIEngineeringImprover(
        FakeChatService(response)
    )

    result = improver.improve(
        improvement_request
    )

    assert len(result.changes) == 2
    assert result.changes[0].content == (
        "def example(value):\n"
        "    return value\n"
    )
    assert result.changes[1].content == (
        "def helper(value):\n"
        "    return value\n"
    )

    assert result.rationale == (
        "Repeated logic was extracted.",
        "The resulting structure is easier to maintain.",
    )


def test_improver_preserves_delete_change(
    improvement_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "brain/obsolete.py",
                    "operation": "delete",
                    "content": "",
                }
            ],
            "rationale": [
                "The obsolete implementation is no longer required."
            ],
        }
    )

    improver = AIEngineeringImprover(
        FakeChatService(response)
    )

    result = improver.improve(
        improvement_request
    )

    assert len(result.changes) == 1
    assert result.changes[0].path == (
        "brain/obsolete.py"
    )
    assert result.changes[0].operation == "delete"
    assert result.changes[0].content == ""


def test_improver_rejects_invalid_change_from_ai(
    improvement_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "rename",
                    "content": "renamed",
                }
            ],
            "rationale": [
                "Invalid improvement."
            ],
        }
    )

    improver = AIEngineeringImprover(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        improver.improve(
            improvement_request
        )


def test_improver_rejects_path_traversal_from_ai(
    improvement_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "../../unsafe.py",
                    "operation": "modify",
                    "content": "unsafe",
                }
            ],
            "rationale": [
                "Invalid improvement."
            ],
        }
    )

    improver = AIEngineeringImprover(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        improver.improve(
            improvement_request
        )


def test_improver_preserves_request_immutability(
    improvement_request,
):
    original_task = improvement_request.task
    original_design = improvement_request.design
    original_plan = improvement_request.plan
    original_code = improvement_request.existing_code
    original_changes = (
        improvement_request.proposed_changes
    )

    improver = AIEngineeringImprover(
        FakeChatService(valid_response())
    )

    improver.improve(
        improvement_request
    )

    assert improvement_request.task is original_task
    assert improvement_request.design is original_design
    assert improvement_request.plan is original_plan
    assert improvement_request.existing_code is original_code
    assert (
        improvement_request.proposed_changes
        == original_changes
    )