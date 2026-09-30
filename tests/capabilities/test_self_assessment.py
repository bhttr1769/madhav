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

def test_assessment_preserves_compatibility_with_capability_contracts():
    capability = CapabilityDescriptor(
        id="web_research",
        name="Web Research",
        description="Research external information.",
        version="1.0.0",
        entry_point="brain.research.ResearchEngine",
        dependencies=frozenset(),
        input_contract="research_query",
        output_contract="research_result",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    assessment = SelfAssessment(
        registry
    ).assess("web_research")

    assert assessment.available is True
    assert assessment.status == "available"
    assert assessment.matched_capabilities == frozenset(
    {"web_research"}
    )

    registered = registry.get(
        "web_research"
    )

    assert registered is capability
    assert registered.input_contract == (
        "research_query"
    )
    assert registered.output_contract == (
        "research_result"
    )

def test_assesses_multiple_available_capabilities():
    capability_a = CapabilityDescriptor(
        id="capability.a",
        name="Capability A",
        description="Test capability A.",
        version="1.0.0",
        entry_point="tests.capabilities.test_self_assessment.TestCapability",
        dependencies=frozenset(),
    )

    capability_b = CapabilityDescriptor(
        id="capability.b",
        name="Capability B",
        description="Test capability B.",
        version="1.0.0",
        entry_point="tests.capabilities.test_self_assessment.TestCapability",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(
            capability_a,
            capability_b,
        ),
    )

    assessment = SelfAssessment(
        registry
    ).assess(
        frozenset({
            "capability.a",
            "capability.b",
        })
    )

    assert assessment.available is True
    assert assessment.status == "available"
    assert assessment.matched_capabilities == frozenset({
        "capability.a",
        "capability.b",
    })
    assert assessment.missing_capabilities == frozenset()


def test_assesses_multiple_capabilities_with_missing_capability():
    capability = CapabilityDescriptor(
        id="capability.a",
        name="Capability A",
        description="Test capability A.",
        version="1.0.0",
        entry_point="tests.capabilities.test_self_assessment.TestCapability",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    assessment = SelfAssessment(
        registry
    ).assess(
        frozenset({
            "capability.a",
            "capability.missing",
        })
    )

    assert assessment.available is False
    assert assessment.status == "unavailable"
    assert assessment.matched_capabilities == frozenset({
        "capability.a",
    })
    assert assessment.missing_capabilities == frozenset({
        "capability.missing",
    })


def test_assessment_preserves_single_capability_compatibility():
    capability = CapabilityDescriptor(
        id="capability.a",
        name="Capability A",
        description="Test capability A.",
        version="1.0.0",
        entry_point="tests.capabilities.test_self_assessment.TestCapability",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    assessment = SelfAssessment(
        registry
    ).assess("capability.a")

    assert assessment.requested_capability == "capability.a"
    assert assessment.available is True
    assert assessment.matched_capabilities == frozenset({
        "capability.a",
    })
    assert assessment.missing_capabilities == frozenset()


def test_assessment_rejects_empty_capability_set():
    registry = CapabilityRegistry(
        capabilities=(),
    )

    with pytest.raises(
        ValueError,
        match="requested_capability must not be empty",
    ):
        SelfAssessment(registry).assess(
            frozenset()
        )


def test_assessment_rejects_non_string_capability_id():
    registry = CapabilityRegistry(
        capabilities=(),
    )

    with pytest.raises(
        TypeError,
        match="requested_capability must contain only strings",
    ):
        SelfAssessment(registry).assess(
            frozenset({
                "valid.capability",
                123,
            })
        )