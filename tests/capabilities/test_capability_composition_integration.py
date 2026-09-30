import pytest

from brain.capabilities.capability_composer import CapabilityComposer
from brain.capabilities.capability_feasibility_checker import (
    CapabilityFeasibilityChecker,
)
from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def create_capability(
    capability_id: str,
    dependencies: frozenset[str] = frozenset(),
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Capability {capability_id}",
        version="1.0.0",
        entry_point=f"brain.{capability_id}.Capability",
        dependencies=dependencies,
    )


def test_feasible_capabilities_can_be_composed():
    first = create_capability("first")
    second = create_capability(
        "second",
        dependencies=frozenset({"first"}),
    )

    capabilities = (
        first,
        second,
    )

    feasibility_checker = CapabilityFeasibilityChecker()

    missing = feasibility_checker.check(
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


def test_infeasible_capabilities_are_rejected_before_composition():
    capability = create_capability(
        "first",
        dependencies=frozenset({"missing"}),
    )

    capabilities = (capability,)

    checker = CapabilityFeasibilityChecker()

    missing = checker.check(
        required_capabilities=frozenset({"first"}),
        available_capabilities=capabilities,
    )

    assert missing == frozenset({"missing"})

    composition = None

    if not missing:
        composition = CapabilityComposer().compose(
            capability_id="composed",
            name="Composed Capability",
            description="A composed capability.",
            version="1.0.0",
            capabilities=capabilities,
        )

    assert composition is None

def test_composition_preserves_original_descriptors_after_feasibility_check():
    first = create_capability("first")
    second = create_capability("second")

    capabilities = (
        first,
        second,
    )

    checker = CapabilityFeasibilityChecker()

    missing = checker.check(
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

    assert composition.capabilities[0] is first
    assert composition.capabilities[1] is second