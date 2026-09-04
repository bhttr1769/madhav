import pytest

from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)


def test_optimization_decision_stores_all_fields():
    decision = OptimizationDecision(
        optimization_justified=True,
        primary_objective="runtime",
        optimization_scope="request processing",
        bottleneck="repeated expensive computation",
        strategies=("reuse computed results", "reduce redundant work"),
        avoid_strategies=("premature micro-optimization",),
        trade_offs=("slightly higher memory usage",),
        measurement_required=True,
        rationale=("The proposed implementation repeats expensive work.",),
    )

    assert decision.optimization_justified is True
    assert decision.primary_objective == "runtime"
    assert decision.optimization_scope == "request processing"
    assert decision.bottleneck == "repeated expensive computation"
    assert decision.strategies == (
        "reuse computed results",
        "reduce redundant work",
    )
    assert decision.avoid_strategies == (
        "premature micro-optimization",
    )
    assert decision.trade_offs == (
        "slightly higher memory usage",
    )
    assert decision.measurement_required is True
    assert decision.rationale == (
        "The proposed implementation repeats expensive work.",
    )


def test_optimization_decision_is_immutable():
    decision = OptimizationDecision(
        optimization_justified=False,
        primary_objective="none",
        optimization_scope="none",
        bottleneck="none identified",
        strategies=(),
        avoid_strategies=("speculative optimization",),
        trade_offs=(),
        measurement_required=False,
        rationale=("No meaningful optimization need was identified.",),
    )

    with pytest.raises(AttributeError):
        decision.optimization_justified = True


def test_optimization_decision_accepts_no_optimization():
    decision = OptimizationDecision(
        optimization_justified=False,
        primary_objective="none",
        optimization_scope="current implementation",
        bottleneck="none identified",
        strategies=(),
        avoid_strategies=("unnecessary optimization",),
        trade_offs=(),
        measurement_required=False,
        rationale=("The implementation is already sufficiently simple.",),
    )

    assert decision.optimization_justified is False
    assert decision.primary_objective == "none"
    assert decision.strategies == ()