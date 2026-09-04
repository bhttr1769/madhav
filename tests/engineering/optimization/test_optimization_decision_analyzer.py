from brain.engineering.optimization.optimization_decision_analyzer import (
    OptimizationDecisionAnalyzer,
)


def test_optimization_decision_analyzer_is_abstract():
    assert OptimizationDecisionAnalyzer.__abstractmethods__ == {
        "analyze"
    }