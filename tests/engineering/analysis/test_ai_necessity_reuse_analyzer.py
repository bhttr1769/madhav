
import json

import pytest

from brain.engineering.analysis.ai_necessity_reuse_analyzer import (
    AINecessityReuseAnalyzer,
)

from brain.engineering.analysis.models.analysis_request import (
    NecessityReuseRequest,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)


class FakeChatService:

    def __init__(self, response):
        self.response = response
        self.prompts = []

    def chat(self, prompt):
        self.prompts.append(prompt)
        return self.response


def make_request(
    task,
    design,
    plan,
    existing_code,
):
    return NecessityReuseRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
    )


def valid_response():
    return json.dumps({
        "necessity": "Implementation is required.",
        "implementation_required": True,
        "reuse_existing": True,
        "use_standard_library": True,
        "use_existing_dependency": False,
        "new_dependency_required": False,
        "abstraction_justified": False,
        "optimization_justified": False,
        "rationale": [
            "An existing project capability can be reused."
        ],
    })


def test_analyzer_requires_chat_method():

    class InvalidChatService:
        pass

    with pytest.raises(
        TypeError,
        match="chat_service must provide a chat method",
    ):
        AINecessityReuseAnalyzer(
            InvalidChatService()
        )


def test_analyzer_requires_analysis_request(
    task_decomposition,
):

    chat_service = FakeChatService(
        valid_response()
    )

    analyzer = AINecessityReuseAnalyzer(
        chat_service
    )

    with pytest.raises(
        TypeError,
        match="request must be a NecessityReuseRequest",
    ):
        analyzer.analyze(
            task_decomposition
        )


def test_analyzer_calls_chat_service(
    task,
    design,
    plan,
    existing_code,
):

    chat_service = FakeChatService(
        valid_response()
    )

    analyzer = AINecessityReuseAnalyzer(
        chat_service
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    analyzer.analyze(request)

    assert len(
        chat_service.prompts
    ) == 1


def test_analyzer_sends_task_to_ai(
    task,
    design,
    plan,
    existing_code,
):

    chat_service = FakeChatService(
        valid_response()
    )

    analyzer = AINecessityReuseAnalyzer(
        chat_service
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    analyzer.analyze(request)

    prompt = chat_service.prompts[0]

    assert task.id in prompt
    assert task.description in prompt


def test_analyzer_sends_existing_code_to_ai(
    task,
    design,
    plan,
    existing_code,
):

    chat_service = FakeChatService(
        valid_response()
    )

    analyzer = AINecessityReuseAnalyzer(
        chat_service
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    analyzer.analyze(request)

    prompt = chat_service.prompts[0]

    for module in existing_code.modules:
        assert str(module) in prompt

    for class_model in existing_code.classes:
        assert str(class_model) in prompt

    for function in existing_code.functions:
        assert str(function) in prompt


def test_analyzer_returns_engineering_decision(
    task,
    design,
    plan,
    existing_code,
):

    chat_service = FakeChatService(
        valid_response()
    )

    analyzer = AINecessityReuseAnalyzer(
        chat_service
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    result = analyzer.analyze(request)

    assert isinstance(
        result,
        EngineeringDecision,
    )
    assert result.implementation_required is True


def test_analyzer_preserves_decision_values(
    task,
    design,
    plan,
    existing_code,
):

    response = json.dumps({
        "necessity": "Existing capability is sufficient.",
        "implementation_required": True,
        "reuse_existing": True,
        "use_standard_library": False,
        "use_existing_dependency": True,
        "new_dependency_required": False,
        "abstraction_justified": True,
        "optimization_justified": False,
        "rationale": [
            "Existing implementation should be reused.",
            "An existing dependency already provides the capability.",
        ],
    })

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(response)
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    result = analyzer.analyze(request)

    assert result.implementation_required is True
    assert result.necessity == (
        "Existing capability is sufficient."
    )
    assert result.reuse_existing is True
    assert result.use_standard_library is False
    assert result.use_existing_dependency is True
    assert result.new_dependency_required is False
    assert result.abstraction_justified is True
    assert result.optimization_justified is False
    assert result.rationale == (
        "Existing implementation should be reused.",
        "An existing dependency already provides the capability.",
    )


def test_analyzer_rejects_invalid_json(
    task,
    design,
    plan,
    existing_code,
):

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService("invalid json")
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        ValueError,
        match="AI response must contain valid JSON",
    ):
        analyzer.analyze(request)


def test_analyzer_rejects_non_object_json(
    task,
    design,
    plan,
    existing_code,
):

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(
            json.dumps([])
        )
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        ValueError,
        match="AI response must be a JSON object",
    ):
        analyzer.analyze(request)


def test_analyzer_rejects_invalid_schema(
    task,
    design,
    plan,
    existing_code,
):

    response = json.dumps({
        "necessity": "required",
    })

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(response)
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        ValueError,
        match="AI response contains an invalid schema",
    ):
        analyzer.analyze(request)


@pytest.mark.parametrize(
    "field",
    [
        "implementation_required",
        "reuse_existing",
        "use_standard_library",
        "use_existing_dependency",
        "new_dependency_required",
        "abstraction_justified",
        "optimization_justified",
    ],
)
def test_analyzer_rejects_non_boolean_decision_fields(
    field,
    task,
    design,
    plan,
    existing_code,
):

    data = json.loads(
        valid_response()
    )

    data[field] = "true"

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(
            json.dumps(data)
        )
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        TypeError,
        match=f"decision {field} must be a boolean",
    ):
        analyzer.analyze(request)


def test_analyzer_rejects_empty_necessity(
    task,
    design,
    plan,
    existing_code,
):

    data = json.loads(
        valid_response()
    )

    data["necessity"] = ""

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(
            json.dumps(data)
        )
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        ValueError,
        match="decision necessity must not be empty",
    ):
        analyzer.analyze(request)


def test_analyzer_rejects_non_list_rationale(
    task,
    design,
    plan,
    existing_code,
):

    data = json.loads(
        valid_response()
    )

    data["rationale"] = "reason"

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(
            json.dumps(data)
        )
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        TypeError,
        match="decision rationale must be a list",
    ):
        analyzer.analyze(request)


def test_analyzer_rejects_empty_rationale_items(
    task,
    design,
    plan,
    existing_code,
):

    data = json.loads(
        valid_response()
    )

    data["rationale"] = [
        "valid",
        "",
    ]

    analyzer = AINecessityReuseAnalyzer(
        FakeChatService(
            json.dumps(data)
        )
    )

    request = make_request(
        task,
        design,
        plan,
        existing_code,
    )

    with pytest.raises(
        ValueError,
        match="decision rationale must not contain empty strings",
    ):
        analyzer.analyze(request)
