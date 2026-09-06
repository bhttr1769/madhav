import json

import pytest

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.review.ai_code_reviewer import AICodeReviewer
from brain.engineering.review.models.code_review_request import (
    CodeReviewRequest as ReviewRequest,
)
from brain.engineering.review.models.code_review_result import (
    CodeReviewResult as ReviewResult,
)
from brain.engineering.tasks.models.task import Task


class FakeChatService:
    def __init__(self, response: str):
        self.response = response
        self.last_prompt = None
        self.call_count = 0

    def chat(self, prompt: str) -> str:
        self.last_prompt = prompt
        self.call_count += 1
        return self.response


def valid_response() -> str:
    return json.dumps(
        {
            "approved": False,
            "findings": [
                {
                    "severity": "high",
                    "category": "correctness",
                    "path": "brain/example.py",
                    "message": "Incorrect behavior.",
                    "recommendation": "Fix the implementation.",
                }
            ],
            "summary": "The implementation requires correction.",
        }
    )


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


@pytest.fixture
def review_request(
    task,
    design,
    plan,
    existing_code,
    proposed_changes,
):
    return ReviewRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
    )


def test_requires_chat_service():
    with pytest.raises(TypeError):
        AICodeReviewer(object())


def test_accepts_chat_service():
    reviewer = AICodeReviewer(
        FakeChatService(valid_response())
    )

    assert reviewer is not None


def test_rejects_invalid_request():
    reviewer = AICodeReviewer(
        FakeChatService(valid_response())
    )

    with pytest.raises(TypeError):
        reviewer.review(object())


def test_calls_chat_service(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    assert chat_service.call_count == 1


def test_prompt_contains_task(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    assert review_request.task.id in chat_service.last_prompt
    assert (
        review_request.task.description
        in chat_service.last_prompt
    )


def test_prompt_contains_acceptance_criteria(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    assert "feature works" in chat_service.last_prompt


def test_prompt_contains_proposed_changes(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    assert "brain/example.py" in chat_service.last_prompt
    assert "def example()" in chat_service.last_prompt


def test_prompt_requires_json(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    assert "Return ONLY valid JSON." in chat_service.last_prompt


def test_returns_review_result(
    review_request,
):
    reviewer = AICodeReviewer(
        FakeChatService(valid_response())
    )

    result = reviewer.review(review_request)

    assert isinstance(result, ReviewResult)


def test_preserves_review_result(
    review_request,
):
    reviewer = AICodeReviewer(
        FakeChatService(valid_response())
    )

    result = reviewer.review(review_request)

    assert result.approved is False
    assert result.summary == (
        "The implementation requires correction."
    )

    assert len(result.findings) == 1

    finding = result.findings[0]

    assert finding.severity == "high"
    assert finding.category == "correctness"
    assert finding.path == "brain/example.py"
    assert finding.message == "Incorrect behavior."
    assert finding.recommendation == "Fix the implementation."


def test_supports_approved_review(
    review_request,
):
    response = json.dumps(
        {
            "approved": True,
            "findings": [],
            "summary": "The implementation is acceptable.",
        }
    )

    reviewer = AICodeReviewer(
        FakeChatService(response)
    )

    result = reviewer.review(review_request)

    assert result.approved is True
    assert result.findings == ()


def test_propagates_invalid_ai_response(
    review_request,
):
    reviewer = AICodeReviewer(
        FakeChatService("{invalid")
    )

    with pytest.raises(ValueError):
        reviewer.review(review_request)


def test_propagates_invalid_response_schema(
    review_request,
):
    reviewer = AICodeReviewer(
        FakeChatService(
            json.dumps(
                {
                    "approved": True,
                    "findings": [],
                    "summary": "ok",
                    "extra": "invalid",
                }
            )
        )
    )

    with pytest.raises(ValueError):
        reviewer.review(review_request)


def test_prompt_contains_review_scope(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    prompt = chat_service.last_prompt

    assert "Do not modify the implementation." in prompt
    assert "Do not generate replacement code." in prompt
    assert "concrete, actionable findings" in prompt

def test_reviewer_passes_multiple_findings_through_parser(
    review_request,
):
    response = json.dumps(
        {
            "approved": False,
            "findings": [
                {
                    "severity": "critical",
                    "category": "security",
                    "path": "brain/example.py",
                    "message": "Security issue.",
                    "recommendation": "Fix the security issue.",
                },
                {
                    "severity": "medium",
                    "category": "maintainability",
                    "path": "brain/example.py",
                    "message": "Implementation is difficult to maintain.",
                    "recommendation": "Simplify the implementation.",
                },
            ],
            "summary": "The implementation requires changes.",
        }
    )

    chat_service = FakeChatService(response)
    reviewer = AICodeReviewer(chat_service)

    result = reviewer.review(review_request)

    assert result.approved is False
    assert len(result.findings) == 2
    assert result.findings[0].severity == "critical"
    assert result.findings[0].category == "security"
    assert result.findings[1].severity == "medium"
    assert result.findings[1].category == "maintainability"


def test_reviewer_preserves_approved_empty_review(
    review_request,
):
    response = json.dumps(
        {
            "approved": True,
            "findings": [],
            "summary": "The implementation is acceptable.",
        }
    )

    reviewer = AICodeReviewer(
        FakeChatService(response)
    )

    result = reviewer.review(review_request)

    assert result.approved is True
    assert result.findings == ()
    assert result.summary == (
        "The implementation is acceptable."
    )


def test_reviewer_rejects_invalid_finding_from_ai(
    review_request,
):
    response = json.dumps(
        {
            "approved": False,
            "findings": [
                {
                    "severity": "critical",
                    "category": "security",
                    "path": "../unsafe.py",
                    "message": "Security issue.",
                    "recommendation": "Fix it.",
                }
            ],
            "summary": "Invalid review.",
        }
    )

    reviewer = AICodeReviewer(
        FakeChatService(response)
    )

    with pytest.raises(ValueError):
        reviewer.review(review_request)


def test_reviewer_sends_complete_engineering_context(
    review_request,
):
    chat_service = FakeChatService(valid_response())
    reviewer = AICodeReviewer(chat_service)

    reviewer.review(review_request)

    prompt = chat_service.last_prompt

    assert review_request.task.id in prompt
    assert (
        review_request.design.requirement.objective
        in prompt
    )
    assert review_request.plan.task_order[0] in prompt

    proposed_change = review_request.proposed_changes[0]

    assert proposed_change.path in prompt
    assert proposed_change.operation in prompt
    assert repr(proposed_change.content) in prompt


def test_reviewer_does_not_require_test_generation_context(
    review_request,
):
    assert hasattr(
        review_request,
        "proposed_changes",
    )

    reviewer = AICodeReviewer(
        FakeChatService(valid_response())
    )

    result = reviewer.review(review_request)

    assert isinstance(result, ReviewResult)