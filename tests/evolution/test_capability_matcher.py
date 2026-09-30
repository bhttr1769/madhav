import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.capability_matcher import (
    CapabilityMatcher,
)


def create_capability(
    capability_id: str,
) -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id=capability_id,
        name=capability_id,
        description=f"Capability {capability_id}",
        version="1.0.0",
        entry_point=(
            f"brain.{capability_id}.Capability"
        ),
        dependencies=frozenset(),
    )


def test_matches_available_capabilities():
    matcher = CapabilityMatcher()

    result = matcher.match(
        required_capabilities=frozenset(
            {
                "file_read",
                "code_analysis",
            }
        ),
        available_capabilities=(
            create_capability("file_read"),
            create_capability("code_analysis"),
            create_capability("test_execution"),
        ),
    )

    assert result == frozenset(
        {
            "file_read",
            "code_analysis",
        }
    )


def test_ignores_missing_capabilities():
    matcher = CapabilityMatcher()

    result = matcher.match(
        required_capabilities=frozenset(
            {
                "file_read",
                "missing",
            }
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == frozenset(
        {"file_read"}
    )


def test_returns_empty_when_nothing_matches():
    matcher = CapabilityMatcher()

    result = matcher.match(
        required_capabilities=frozenset(
            {"missing"},
        ),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == frozenset()


def test_returns_empty_for_no_requirements():
    matcher = CapabilityMatcher()

    result = matcher.match(
        required_capabilities=frozenset(),
        available_capabilities=(
            create_capability("file_read"),
        ),
    )

    assert result == frozenset()


def test_rejects_non_frozenset_requirements():
    matcher = CapabilityMatcher()

    with pytest.raises(
        TypeError,
        match="required_capabilities must be a frozenset",
    ):
        matcher.match(
            required_capabilities={"file_read"},
            available_capabilities=(),
        )


def test_rejects_non_tuple_capabilities():
    matcher = CapabilityMatcher()

    with pytest.raises(
        TypeError,
        match="available_capabilities must be a tuple",
    ):
        matcher.match(
            required_capabilities=frozenset(
                {"file_read"},
            ),
            available_capabilities=[
                create_capability("file_read"),
            ],
        )


def test_rejects_invalid_capability():
    matcher = CapabilityMatcher()

    with pytest.raises(
        TypeError,
        match="CapabilityDescriptor",
    ):
        matcher.match(
            required_capabilities=frozenset(
                {"file_read"},
            ),
            available_capabilities=("invalid",),
        )

def test_matcher_preserves_capability_contracts():
    capability = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability",
        version="1.0.0",
        entry_point="brain.test.TestCapability",
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    matcher = CapabilityMatcher()

    result = matcher.match(
        required_capabilities=frozenset(
            {"test.capability"}
        ),
        available_capabilities=(
            capability,
        ),
    )

    assert result == frozenset(
        {"test.capability"}
    )

    assert capability.input_contract == "text"
    assert capability.output_contract == "number"