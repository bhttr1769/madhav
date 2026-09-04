import json

import pytest

from brain.engineering.optimization.ai_optimization_decision_analyzer import (
    AIOptimizationDecisionAnalyzer,
)
from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)
from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)


class FakeChatService:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def chat(self, prompt):
        self.calls.append(prompt)
        return self.response


def _request():
    return OptimizationDecisionRequest(
        task=object(),
        design=object(),
        plan=object(),
        engineering_decision=object(),
        quality_assessment=object(),
        existing_code=object(),
        proposed_changes=(),
    )


def _valid_payload():
    return {
        "optimization_justified": True,
        "primary_objective": "runtime",
        "optimization_scope": "request processing",
        "bottleneck": "repeated expensive computation",
        "strategies": [
            "reuse computed results",
            "reduce redundant work",
        ],
        "avoid_strategies": [
            "speculative micro-optimization",
        ],
        "trade_offs": [
            "slightly higher memory usage",
        ],
        "measurement_required": True,
        "rationale": [
            "The proposed implementation repeats expensive work.",
        ],
    }


def test_analyzer_requires_chat_service():
    with pytest.raises(TypeError):
        AIOptimizationDecisionAnalyzer(None)


def test_analyzer_requires_chat_method():
    class InvalidChatService:
        pass

    with pytest.raises(TypeError):
        AIOptimizationDecisionAnalyzer(InvalidChatService())


def test_analyzer_requires_correct_request_type():
    service = FakeChatService(json.dumps(_valid_payload()))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(TypeError):
        analyzer.analyze(object())


def test_analyzer_returns_optimization_decision():
    service = FakeChatService(json.dumps(_valid_payload()))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    result = analyzer.analyze(_request())

    assert isinstance(result, OptimizationDecision)
    assert result.optimization_justified is True
    assert result.primary_objective == "runtime"
    assert result.optimization_scope == "request processing"
    assert result.bottleneck == "repeated expensive computation"
    assert result.strategies == (
        "reuse computed results",
        "reduce redundant work",
    )
    assert result.avoid_strategies == (
        "speculative micro-optimization",
    )
    assert result.trade_offs == (
        "slightly higher memory usage",
    )
    assert result.measurement_required is True
    assert result.rationale == (
        "The proposed implementation repeats expensive work.",
    )


def test_analyzer_accepts_dictionary_response():
    service = FakeChatService(_valid_payload())
    analyzer = AIOptimizationDecisionAnalyzer(service)

    result = analyzer.analyze(_request())

    assert isinstance(result, OptimizationDecision)


def test_analyzer_rejects_invalid_json():
    service = FakeChatService("not valid json")
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_non_object_response():
    service = FakeChatService(json.dumps(["invalid"]))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_missing_field():
    payload = _valid_payload()
    del payload["bottleneck"]

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_extra_field():
    payload = _valid_payload()
    payload["unexpected"] = "value"

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_invalid_optimization_justified_type():
    payload = _valid_payload()
    payload["optimization_justified"] = "true"

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_invalid_measurement_required_type():
    payload = _valid_payload()
    payload["measurement_required"] = "true"

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_invalid_primary_objective():
    payload = _valid_payload()
    payload["primary_objective"] = "random"

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_empty_required_string():
    payload = _valid_payload()
    payload["bottleneck"] = "   "

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_non_list_strategies():
    payload = _valid_payload()
    payload["strategies"] = "reuse results"

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_empty_strategy_entry():
    payload = _valid_payload()
    payload["strategies"] = [""]

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_requires_strategies_when_optimization_is_justified():
    payload = _valid_payload()
    payload["strategies"] = []

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_requires_none_objective_when_optimization_is_not_justified():
    payload = _valid_payload()
    payload["optimization_justified"] = False
    payload["primary_objective"] = "runtime"
    payload["strategies"] = []

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_rejects_strategies_when_optimization_is_not_justified():
    payload = _valid_payload()
    payload["optimization_justified"] = False
    payload["primary_objective"] = "none"

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    with pytest.raises(ValueError):
        analyzer.analyze(_request())


def test_analyzer_accepts_no_optimization_decision():
    payload = _valid_payload()
    payload["optimization_justified"] = False
    payload["primary_objective"] = "none"
    payload["strategies"] = []
    payload["measurement_required"] = False
    payload["bottleneck"] = "none identified"
    payload["optimization_scope"] = "current implementation"
    payload["rationale"] = [
        "No meaningful optimization need was identified."
    ]

    service = FakeChatService(json.dumps(payload))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    result = analyzer.analyze(_request())

    assert result.optimization_justified is False
    assert result.primary_objective == "none"
    assert result.strategies == ()
    assert result.measurement_required is False


def test_analyzer_passes_complete_engineering_context_to_chat_service():
    request = _request()

    service = FakeChatService(json.dumps(_valid_payload()))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    analyzer.analyze(request)

    assert len(service.calls) == 1

    prompt = service.calls[0]

    assert repr(request.task) in prompt
    assert repr(request.design) in prompt
    assert repr(request.plan) in prompt
    assert repr(request.engineering_decision) in prompt
    assert repr(request.quality_assessment) in prompt
    assert repr(request.existing_code) in prompt
    assert repr(request.proposed_changes) in prompt


def test_analyzer_prompt_forbids_code_generation_and_file_modification():
    service = FakeChatService(json.dumps(_valid_payload()))
    analyzer = AIOptimizationDecisionAnalyzer(service)

    analyzer.analyze(_request())

    prompt = service.calls[0]

    assert "Do not generate source code" in prompt
    assert "Do not modify or rewrite the proposed changes" in prompt
    assert "Do not install or introduce dependencies" in prompt
    assert "Do not perform benchmarking" in prompt
    assert "Remain language-agnostic" in prompt