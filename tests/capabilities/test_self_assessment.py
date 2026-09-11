import pytest

from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.capabilities.self_assessment import (
    SelfAssessment,
)


def _capability(
    capability_id="web_research",
):
    return CapabilityDescriptor(
        id=capability_id,
        name="Web Research",
        description="Research external information.",
        version="1.0.0",
        entry_point="brain.research.ResearchEngine",
        dependencies=frozenset(),
    )


def test_assessment_reports_available_capability():
    registry = CapabilityRegistry(
        capabilities=(
            _capability(),
        ),
    )

    assessment = SelfAssessment(
        registry
    ).assess("web_research")

    assert isinstance(
        assessment,
        CapabilityAssessment,
    )

    assert assessment.requested_capability == (
        "web_research"
    )
    assert assessment.available is True
    assert assessment.status == "available"
    assert assessment.matched_capabilities == (
        frozenset({"web_research"})
    )
    assert assessment.missing_capabilities == (
        frozenset()
    )


def test_assessment_reports_unavailable_capability():
    registry = CapabilityRegistry()

    assessment = SelfAssessment(
        registry
    ).assess("web_research")

    assert assessment.available is False
    assert assessment.status == "unavailable"
    assert assessment.matched_capabilities == (
        frozenset()
    )
    assert assessment.missing_capabilities == (
        frozenset({"web_research"})
    )


def test_assessment_provides_rationale():
    registry = CapabilityRegistry()

    assessment = SelfAssessment(
        registry
    ).assess("web_research")

    assert assessment.rationale == (
        "The requested capability is not registered."
    )


def test_assessment_rejects_invalid_registry():
    with pytest.raises(TypeError):
        SelfAssessment(None)


def test_assessment_rejects_non_string_request():
    registry = CapabilityRegistry()

    assessor = SelfAssessment(registry)

    with pytest.raises(TypeError):
        assessor.assess(None)


def test_assessment_rejects_empty_request():
    registry = CapabilityRegistry()

    assessor = SelfAssessment(registry)

    with pytest.raises(ValueError):
        assessor.assess("")


def test_assessment_rejects_whitespace_request():
    registry = CapabilityRegistry()

    assessor = SelfAssessment(registry)

    with pytest.raises(ValueError):
        assessor.assess("   ")