import json

import pytest

from brain.engineering.debugging.ai_debugger import AIDebugger
from brain.engineering.debugging.models.debugging_request import (
    DebuggingRequest,
)
from brain.engineering.debugging.models.debugging_result import (
    DebuggingResult,
)
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task
from brain.engineering.requirements.models.requirement import Requirement
from brain.code.models.code_structure import CodeStructure


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
                    "content": "return fixed_value",
                }
            ],
            "diagnosis": (
                "The failure was caused by an undefined variable."
            ),
        }
    )


@pytest.fixture
def debugging_request():
    requirement = Requirement(
        original_request="Fix the failing implementation.",
        objective="Resolve the implementation failure.",
        functional_requirements=frozenset(
            {"the failure must be resolved"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"the implementation executes successfully"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({"brain/example.py"}),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Fix failing implementation",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({"brain/example.py"}),
        acceptance_criteria=frozenset(
            {"failure is resolved"}
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
            {"implementation executes successfully"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("identify root cause", "apply minimal fix"),
        milestones=("debugging",),
        required_capabilities=frozenset(
            {"debugging"}
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

    return DebuggingRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
        error_message=(
            "NameError: name 'value' is not defined"
        ),
        traceback=(
            "Traceback (most recent call last): ..."
        ),
    )


def test_debugger_returns_parsed_result(
    debugging_request,
):
    debugger = AIDebugger(
        FakeChatService(valid_response())
    )

    result = debugger.debug(debugging_request)

    assert isinstance(result, DebuggingResult)
    assert len(result.changes) == 1
    assert result.changes[0].path == (
        "brain/example.py"
    )
    assert result.diagnosis == (
        "The failure was caused by an undefined variable."
    )


def test_debugger_calls_chat_service(
    debugging_request,
):
    chat_service = FakeChatService(
        valid_response()
    )
    debugger = AIDebugger(chat_service)

    debugger.debug(debugging_request)

    assert chat_service.last_prompt is not None
    assert chat_service.last_prompt.strip()


def test_debugger_rejects_invalid_request():
    debugger = AIDebugger(
        FakeChatService(valid_response())
    )

    with pytest.raises(TypeError):
        debugger.debug(None)


def test_debugger_rejects_invalid_ai_response(
    debugging_request,
):
    debugger = AIDebugger(
        FakeChatService("not valid json")
    )

    with pytest.raises(ValueError):
        debugger.debug(debugging_request)


def test_debugger_passes_multiple_changes_through_parser(
    debugging_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": "return fixed_value",
                },
                {
                    "path": "tests/example.py",
                    "operation": "modify",
                    "content": "assert result == expected",
                },
            ],
            "diagnosis": (
                "The implementation and its test "
                "required correction."
            ),
        }
    )

    debugger = AIDebugger(
        FakeChatService(response)
    )

    result = debugger.debug(debugging_request)

    assert len(result.changes) == 2
    assert result.changes[0].path == (
        "brain/example.py"
    )
    assert result.changes[1].path == (
        "tests/example.py"
    )


def test_debugger_sends_complete_engineering_context(
    debugging_request,
):
    chat_service = FakeChatService(
        valid_response()
    )
    debugger = AIDebugger(chat_service)

    debugger.debug(debugging_request)

    prompt = chat_service.last_prompt

    assert debugging_request.task.id in prompt
    assert (
        debugging_request.design.requirement.objective
        in prompt
    )
    assert debugging_request.plan.task_order[0] in prompt
    assert (
        debugging_request.error_message
        in prompt
    )
    assert debugging_request.traceback in prompt

    proposed_change = (
        debugging_request.proposed_changes[0]
    )

    assert proposed_change.path in prompt
    assert proposed_change.operation in prompt
    assert repr(proposed_change.content) in prompt


def test_debugger_does_not_execute_code(
    debugging_request,
):
    chat_service = FakeChatService(
        valid_response()
    )
    debugger = AIDebugger(chat_service)

    result = debugger.debug(debugging_request)

    assert isinstance(result, DebuggingResult)

def test_debugger_preserves_diagnosis_and_all_changes(
    debugging_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "brain/example.py",
                    "operation": "modify",
                    "content": "return corrected_value",
                },
                {
                    "path": "tests/example.py",
                    "operation": "modify",
                    "content": "assert result == expected",
                },
                {
                    "path": "brain/unused.py",
                    "operation": "delete",
                    "content": "",
                },
            ],
            "diagnosis": (
                "The failure originated from an undefined "
                "variable and an outdated test expectation."
            ),
        }
    )

    debugger = AIDebugger(
        FakeChatService(response)
    )

    result = debugger.debug(debugging_request)

    assert result.diagnosis == (
        "The failure originated from an undefined "
        "variable and an outdated test expectation."
    )
    assert len(result.changes) == 3

    assert result.changes[0].path == (
        "brain/example.py"
    )
    assert result.changes[0].operation == "modify"

    assert result.changes[1].path == (
        "tests/example.py"
    )
    assert result.changes[1].operation == "modify"

    assert result.changes[2].path == (
        "brain/unused.py"
    )
    assert result.changes[2].operation == "delete"


def test_debugger_propagates_parser_validation_failure(
    debugging_request,
):
    response = json.dumps(
        {
            "changes": [
                {
                    "path": "../outside.py",
                    "operation": "modify",
                    "content": "unsafe",
                }
            ],
            "diagnosis": "Invalid change.",
        }
    )

    debugger = AIDebugger(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        debugger.debug(debugging_request)


def test_debugger_handles_no_change_diagnosis(
    debugging_request,
):
    response = json.dumps(
        {
            "changes": [],
            "diagnosis": (
                "The reported failure is caused by an "
                "external condition and requires no code change."
            ),
        }
    )

    debugger = AIDebugger(
        FakeChatService(response)
    )

    result = debugger.debug(debugging_request)

    assert result.changes == ()
    assert result.diagnosis == (
        "The reported failure is caused by an "
        "external condition and requires no code change."
    )


def test_debugger_uses_exact_chat_response(
    debugging_request,
):
    response = valid_response()
    chat_service = FakeChatService(response)

    debugger = AIDebugger(chat_service)
    result = debugger.debug(debugging_request)

    assert result.changes[0].content == (
        "return fixed_value"
    )