import pytest

from brain.engineering.optimization.fake_optimization_decision_analyzer import (
    FakeOptimizationDecisionAnalyzer,
)
from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)
from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)


def decision():
    return OptimizationDecision(
        optimization_justified=True,
        primary_objective="runtime",
        optimization_scope="request processing",
        bottleneck="repeated expensive computation",
        strategies=("reuse computed results",),
        avoid_strategies=("speculative optimization",),
        trade_offs=("slightly higher memory usage",),
        measurement_required=True,
        rationale=("Optimization is justified by repeated work.",),
    )


def request():
    return OptimizationDecisionRequest(
        task=object(),
        design=object(),
        plan=object(),
        engineering_decision=object(),
        quality_assessment=object(),
        existing_code=object(),
        proposed_changes=(),
    )


def test_fake_analyzer_returns_configured_decision():
    configured = decision()

    analyzer = FakeOptimizationDecisionAnalyzer(
        configured,
    )

    result = analyzer.analyze(
        request(),
    )

    assert result is configured


def test_fake_analyzer_preserves_request():
    configured = decision()
    engineering_request = request()

    analyzer = FakeOptimizationDecisionAnalyzer(
        configured,
    )

    analyzer.analyze(
        engineering_request,
    )

    assert analyzer.last_request is engineering_request


def test_fake_analyzer_requires_optimization_decision():
    with pytest.raises(TypeError):
        FakeOptimizationDecisionAnalyzer(
            object(),
        )


def test_fake_analyzer_rejects_invalid_request():
    analyzer = FakeOptimizationDecisionAnalyzer(
        decision(),
    )

    with pytest.raises(TypeError):
        analyzer.analyze(
            object(),
        )