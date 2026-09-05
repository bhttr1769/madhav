import pytest

from brain.engineering.analysis.necessity_reuse_analyzer import (
    NecessityReuseAnalyzer,
)
from brain.engineering.analysis.fake_necessity_reuse_analyzer import (
    FakeNecessityReuseAnalyzer,
)
from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)


def _decision():
    return EngineeringDecision(
        implementation_required=True,
        necessity="existing capability is insufficient",
        reuse_existing=True,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "Existing project capability should be reused.",
        ),
    )


def test_analyzer_is_abstract():
    with pytest.raises(TypeError):
        NecessityReuseAnalyzer()


def test_fake_analyzer_returns_configured_result():
    result = _decision()

    analyzer = FakeNecessityReuseAnalyzer(result)

    returned = analyzer.analyze(
        task=object(),
        design=object(),
        code_structure=object(),
    )

    assert returned is result


def test_fake_analyzer_is_an_analyzer():
    assert issubclass(
        FakeNecessityReuseAnalyzer,
        NecessityReuseAnalyzer,
    )