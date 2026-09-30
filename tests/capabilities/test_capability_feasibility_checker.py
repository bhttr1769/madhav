import pytest

from brain.capabilities.capability_feasibility_checker import (
    CapabilityFeasibilityChecker,
)
from brain.capabilities.models.capability_descriptor import CapabilityDescriptor


def create_capability(
    capability_id: str,
    dependencies: frozenset[str] = frozenset(),
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Test capability {capability_id}",
        version="1.0.0",
        entry_point="test.module:execute",
        dependencies=dependencies,
    )


def test_returns_empty_when_capabilities_are_available():
    capability = create_capability("capability.a")

    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset({"capability.a"}),
        available_capabilities=(capability,),
    )

    assert result == frozenset()


def test_detects_missing_requested_capability():
    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset({"capability.a"}),
        available_capabilities=(),
    )

    assert result == frozenset({"capability.a"})


def test_detects_missing_direct_dependency():
    capability = create_capability(
        "capability.a",
        dependencies=frozenset({"capability.b"}),
    )

    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset({"capability.a"}),
        available_capabilities=(capability,),
    )

    assert result == frozenset({"capability.b"})


def test_detects_missing_transitive_dependency():
    capability_a = create_capability(
        "capability.a",
        dependencies=frozenset({"capability.b"}),
    )

    capability_b = create_capability(
        "capability.b",
        dependencies=frozenset({"capability.c"}),
    )

    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset({"capability.a"}),
        available_capabilities=(capability_a, capability_b),
    )

    assert result == frozenset({"capability.c"})


def test_returns_empty_when_transitive_dependencies_are_available():
    capability_a = create_capability(
        "capability.a",
        dependencies=frozenset({"capability.b"}),
    )

    capability_b = create_capability(
        "capability.b",
        dependencies=frozenset({"capability.c"}),
    )

    capability_c = create_capability("capability.c")

    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset({"capability.a"}),
        available_capabilities=(
            capability_a,
            capability_b,
            capability_c,
        ),
    )

    assert result == frozenset()


def test_detects_multiple_missing_dependencies():
    capability = create_capability(
        "capability.a",
        dependencies=frozenset(
            {
                "capability.b",
                "capability.c",
            }
        ),
    )

    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset({"capability.a"}),
        available_capabilities=(capability,),
    )

    assert result == frozenset(
        {
            "capability.b",
            "capability.c",
        }
    )


def test_detects_missing_dependency_across_multiple_requested_capabilities():
    capability_a = create_capability(
        "capability.a",
        dependencies=frozenset({"capability.b"}),
    )

    capability_c = create_capability(
        "capability.c",
        dependencies=frozenset({"capability.d"}),
    )

    checker = CapabilityFeasibilityChecker()

    result = checker.check(
        required_capabilities=frozenset(
            {
                "capability.a",
                "capability.c",
            }
        ),
        available_capabilities=(
            capability_a,
            capability_c,
        ),
    )

    assert result == frozenset(
        {
            "capability.b",
            "capability.d",
        }
    )


def test_preserves_dependency_cycle_detection():
    capability_a = create_capability(
        "capability.a",
        dependencies=frozenset({"capability.b"}),
    )

    capability_b = create_capability(
        "capability.b",
        dependencies=frozenset({"capability.a"}),
    )

    checker = CapabilityFeasibilityChecker()

    with pytest.raises(
        ValueError,
        match="cyclic capability dependency detected",
    ):
        checker.check(
            required_capabilities=frozenset({"capability.a"}),
            available_capabilities=(
                capability_a,
                capability_b,
            ),
        )


def test_rejects_invalid_required_capabilities_type():
    checker = CapabilityFeasibilityChecker()

    with pytest.raises(
        TypeError,
        match="required_capabilities must be a frozenset",
    ):
        checker.check(
            required_capabilities={"capability.a"},
            available_capabilities=(),
        )


def test_rejects_non_string_required_capability():
    checker = CapabilityFeasibilityChecker()

    with pytest.raises(
        TypeError,
        match="required_capabilities must contain only strings",
    ):
        checker.check(
            required_capabilities=frozenset({123}),
            available_capabilities=(),
        )


def test_rejects_invalid_available_capabilities_type():
    checker = CapabilityFeasibilityChecker()

    with pytest.raises(
        TypeError,
        match="available_capabilities must be a tuple",
    ):
        checker.check(
            required_capabilities=frozenset({"capability.a"}),
            available_capabilities=[],
        )


def test_rejects_non_descriptor_available_capability():
    checker = CapabilityFeasibilityChecker()

    with pytest.raises(
        TypeError,
        match="available_capabilities must contain only "
        "CapabilityDescriptor instances",
    ):
        checker.check(
            required_capabilities=frozenset({"capability.a"}),
            available_capabilities=("capability.a",),
        )