import pytest

from brain.capabilities.capability_composer import CapabilityComposer
from brain.capabilities.capability_feasibility_checker import (
    CapabilityFeasibilityChecker,
)
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.capabilities.self_assessment import SelfAssessment


def create_capability(
    capability_id: str,
    dependencies: frozenset[str] = frozenset(),
    input_contract: str = "object",
    output_contract: str = "object",
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Capability {capability_id}",
        version="1.0.0",
        entry_point=f"brain.{capability_id}.Capability",
        dependencies=dependencies,
        input_contract=input_contract,
        output_contract=output_contract,
    )


def test_available_capabilities_are_assessed_and_composed():
    first = create_capability("first")
    second = create_capability(
        "second",
        dependencies=frozenset({"first"}),
    )

    capabilities = (
        first,
        second,
    )

    registry = CapabilityRegistry(
        capabilities=capabilities,
    )

    assessment = SelfAssessment(registry).assess(
        frozenset(
            {
                "first",
                "second",
            }
        )
    )

    assert isinstance(
        assessment,
        CapabilityAssessment,
    )

    assert assessment.available is True
    assert assessment.status == "available"
    assert assessment.missing_capabilities == frozenset()
    assert assessment.matched_capabilities == frozenset(
        {
            "first",
            "second",
        }
    )

    missing = CapabilityFeasibilityChecker().check(
        required_capabilities=frozenset(
            {
                "first",
                "second",
            }
        ),
        available_capabilities=capabilities,
    )

    assert missing == frozenset()

    composition = CapabilityComposer().compose(
        capability_id="composed",
        name="Composed Capability",
        description="A composed capability.",
        version="1.0.0",
        capabilities=capabilities,
    )

    assert isinstance(
        composition,
        CapabilityComposition,
    )

    assert composition.capabilities == capabilities


def test_missing_capability_is_reported_by_assessment():
    registered = create_capability("first")

    registry = CapabilityRegistry(
        capabilities=(registered,),
    )

    assessment = SelfAssessment(registry).assess(
        frozenset(
            {
                "first",
                "missing",
            }
        )
    )

    assert assessment.available is False
    assert assessment.status == "unavailable"
    assert assessment.matched_capabilities == frozenset(
        {"first"}
    )
    assert assessment.missing_capabilities == frozenset(
        {"missing"}
    )


def test_missing_dependency_is_reported_by_feasibility_check():
    capability = create_capability(
        "first",
        dependencies=frozenset({"missing"}),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    assessment = SelfAssessment(registry).assess(
        "first"
    )

    assert assessment.available is True
    assert assessment.missing_capabilities == frozenset()

    missing = CapabilityFeasibilityChecker().check(
        required_capabilities=frozenset({"first"}),
        available_capabilities=(capability,),
    )

    assert missing == frozenset({"missing"})


def test_transitive_missing_dependency_is_reported():
    first = create_capability(
        "first",
        dependencies=frozenset({"second"}),
    )

    second = create_capability(
        "second",
        dependencies=frozenset({"missing"}),
    )

    capabilities = (
        first,
        second,
    )

    missing = CapabilityFeasibilityChecker().check(
        required_capabilities=frozenset({"first"}),
        available_capabilities=capabilities,
    )

    assert missing == frozenset({"missing"})


def test_dependency_cycle_is_rejected():
    first = create_capability(
        "first",
        dependencies=frozenset({"second"}),
    )

    second = create_capability(
        "second",
        dependencies=frozenset({"first"}),
    )

    with pytest.raises(
        ValueError,
        match="cyclic capability dependency detected",
    ):
        CapabilityFeasibilityChecker().check(
            required_capabilities=frozenset({"first"}),
            available_capabilities=(
                first,
                second,
            ),
        )


def test_composition_preserves_descriptor_identity_and_contracts():
    first = create_capability(
        "first",
        input_contract="text",
        output_contract="number",
    )

    second = create_capability(
        "second",
        input_contract="number",
        output_contract="text",
    )

    composition = CapabilityComposer().compose(
        capability_id="pipeline",
        name="Pipeline",
        description="Test pipeline.",
        version="1.0.0",
        capabilities=(
            first,
            second,
        ),
    )

    assert composition.capabilities[0] is first
    assert composition.capabilities[1] is second

    assert composition.capabilities[0].input_contract == "text"
    assert composition.capabilities[0].output_contract == "number"

    assert composition.capabilities[1].input_contract == "number"
    assert composition.capabilities[1].output_contract == "text"