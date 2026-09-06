import json

import pytest

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.refactoring.ai_refactorer import AIRefactorer
from brain.engineering.refactoring.models.refactoring_request import (
    RefactoringRequest,
)
from brain.engineering.refactoring.models.refactoring_result import (
    RefactoringResult,
)
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
            "rationale": (
                "The implementation was simplified "
                "without changing behavior."
            ),
        }
    )


@pytest.fixture
def refactoring_request():
    requirement = Requirement(
        original_request="Improve the implementation.",
        objective="Improve maintainability without changing behavior.",
        functional_requirements=frozenset(
            {"existing behavior must be preserved"}
        ),
        non_functional_requirements=frozenset(
            {"improve maintainability"}
        ),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"behavior remains unchanged"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({"brain/example.py"}),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Improve implementation structure",
        category="refactoring",
        dependencies=frozenset(),
        affected_areas=frozenset({"brain/example.py"}),
        acceptance_criteria=frozenset(
            {"behavior remains unchanged"}
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
            {"behavior remains unchanged"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("improve maintainability",),
        milestones=("refactoring",),
        required_capabilities=frozenset(
            {"refactoring"}
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

    return RefactoringRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
    )


def test_refactorer_returns_parsed_result(
    refactoring_request,
):
    refactorer = AIRefactorer(
        FakeChatService(valid_response())
    )

    result = refactorer.refactor(
        refactoring_request
    )

    assert isinstance(result, RefactoringResult)
    assert len(result.changes) == 1
    assert result.changes[0].path == (
        "brain/example.py"
    )
    assert result.changes[0].operation == "modify"
    assert result.rationale == (
        "The implementation was simplified "
        "without changing behavior."
    )


def test_refactorer_calls_chat_service(
    refactoring_request,
):
    chat_service = FakeChatService(
        valid_response()
    )
    refactorer = AIRefactorer(chat_service)

    refactorer.refactor(refactoring_request)

    assert chat_service.last_prompt is not None
    assert chat_service.last_prompt.strip()


def test_refactorer_rejects_invalid_request():
    refactorer = AIRefactorer(
        FakeChatService(valid_response())
    )

    with pytest.raises(TypeError):
        refactorer.refactor(None)


def test_refactorer_rejects_invalid_ai_response(
    refactoring_request,
):
    refactorer = AIRefactorer(
        FakeChatService("not valid json")
    )

    with pytest.raises(ValueError):
        refactorer.refactor(refactoring_request)


def test_refactorer_passes_multiple_changes_through_parser(
    refactoring_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": "return value",
                },
                {
                    "path": "brain/helper.py",
                    "operation": "create",
                    "content": "def helper():\n    return True",
                },
            ],
            "rationale": (
                "The implementation was simplified "
                "and a repeated operation was extracted."
            ),
        }
    )

    refactorer = AIRefactorer(
        FakeChatService(response)
    )

    result = refactorer.refactor(
        refactoring_request
    )

    assert len(result.changes) == 2
    assert result.changes[0].path == (
        "brain/example.py"
    )
    assert result.changes[1].path == (
        "brain/helper.py"
    )


def test_refactorer_handles_no_refactoring_required(
    refactoring_request,
):
    response = json.dumps(
        {
            "changes": [],
            "rationale": (
                "The implementation is already sufficiently "
                "simple and no refactoring is justified."
            ),
        }
    )

    refactorer = AIRefactorer(
        FakeChatService(response)
    )

    result = refactorer.refactor(
        refactoring_request
    )

    assert result.changes == ()
    assert result.rationale == (
        "The implementation is already sufficiently "
        "simple and no refactoring is justified."
    )


def test_refactorer_sends_complete_engineering_context(
    refactoring_request,
):
    chat_service = FakeChatService(
        valid_response()
    )
    refactorer = AIRefactorer(chat_service)

    refactorer.refactor(refactoring_request)

    prompt = chat_service.last_prompt

    assert refactoring_request.task.id in prompt
    assert (
        refactoring_request.design.requirement.objective
        in prompt
    )
    assert (
        refactoring_request.plan.task_order[0]
        in prompt
    )

    proposed_change = (
        refactoring_request.proposed_changes[0]
    )

    assert proposed_change.path in prompt
    assert proposed_change.operation in prompt
    assert repr(proposed_change.content) in prompt


def test_refactorer_preserves_parser_validation_boundary(
    refactoring_request,
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
            "rationale": "Invalid refactoring.",
        }
    )

    refactorer = AIRefactorer(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        refactorer.refactor(
            refactoring_request
        )


def test_refactorer_does_not_execute_code(
    refactoring_request,
):
    refactorer = AIRefactorer(
        FakeChatService(valid_response())
    )

    result = refactorer.refactor(
        refactoring_request
    )

    assert isinstance(result, RefactoringResult)

def test_refactorer_preserves_all_change_content(
    refactoring_request,
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
            "rationale": (
                "Repeated logic was extracted into a "
                "small reusable helper."
            ),
        }
    )

    refactorer = AIRefactorer(
        FakeChatService(response)
    )

    result = refactorer.refactor(
        refactoring_request
    )

    assert result.changes[0].content == (
        "def example(value):\n"
        "    return value\n"
    )
    assert result.changes[1].content == (
        "def helper(value):\n"
        "    return value\n"
    )


def test_refactorer_preserves_delete_change(
    refactoring_request,
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
            "rationale": (
                "The obsolete module is no longer required."
            ),
        }
    )

    refactorer = AIRefactorer(
        FakeChatService(response)
    )

    result = refactorer.refactor(
        refactoring_request
    )

    assert len(result.changes) == 1
    assert result.changes[0].path == (
        "brain/obsolete.py"
    )
    assert result.changes[0].operation == "delete"
    assert result.changes[0].content == ""


def test_refactorer_rejects_invalid_change_from_ai(
    refactoring_request,
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
            "rationale": "Invalid refactoring.",
        }
    )

    refactorer = AIRefactorer(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        refactorer.refactor(
            refactoring_request
        )


def test_refactorer_does_not_modify_request(
    refactoring_request,
):
    original_changes = (
        refactoring_request.proposed_changes
    )

    refactorer = AIRefactorer(
        FakeChatService(valid_response())
    )

    refactorer.refactor(refactoring_request)

    assert (
        refactoring_request.proposed_changes
        == original_changes
    )