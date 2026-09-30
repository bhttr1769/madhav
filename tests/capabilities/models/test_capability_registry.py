import pytest

from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def _capability(
    capability_id="test",
):
    return CapabilityDescriptor(
        id=capability_id,
        name="Test Capability",
        description="A test capability.",
        version="1.0.0",
        entry_point="brain.test.Test",
        dependencies=frozenset(),
    )


def test_registry_starts_empty():
    registry = CapabilityRegistry()

    assert registry.all() == ()
    

def test_registry_registers_capability():
    registry = CapabilityRegistry()
    capability = _capability()

    registry.register(capability)

    assert registry.has("test")
    assert registry.get("test") == capability
    assert registry.all() == (capability,)


def test_registry_accepts_initial_capabilities():
    first = _capability("first")
    second = _capability("second")

    registry = CapabilityRegistry(
        capabilities=(first, second),
    )

    assert registry.all() == (
        first,
        second,
    )


def test_registry_rejects_invalid_capability():
    registry = CapabilityRegistry()

    with pytest.raises(TypeError):
        registry.register("invalid")


def test_registry_rejects_duplicate_capability():
    registry = CapabilityRegistry()

    registry.register(_capability())

    with pytest.raises(ValueError):
        registry.register(_capability())


def test_registry_reports_missing_capability():
    registry = CapabilityRegistry()

    assert registry.has("missing") is False


def test_registry_get_rejects_missing_capability():
    registry = CapabilityRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_registry_returns_immutable_snapshot():
    registry = CapabilityRegistry()

    capability = _capability()
    registry.register(capability)

    capabilities = registry.all()

    assert isinstance(capabilities, tuple)
    assert capabilities == (capability,)


def test_registry_unregisters_capability():
    registry = CapabilityRegistry()

    registry.register(_capability())

    registry.unregister("test")

    assert registry.has("test") is False
    assert registry.all() == ()


def test_registry_unregister_rejects_missing_capability():
    registry = CapabilityRegistry()

    with pytest.raises(KeyError):
        registry.unregister("missing")

def test_registry_preserves_contracts() -> None:
    capability = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    registry = CapabilityRegistry()

    registry.register(capability)

    registered = registry.get(
        "test.capability"
    )

    assert registered is capability
    assert registered.input_contract == "text"
    assert registered.output_contract == "number"

def test_registry_all_preserves_contracts() -> None:
    capability = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,)
    )

    registered = registry.all()

    assert registered == (capability,)
    assert registered[0].input_contract == "text"
    assert registered[0].output_contract == "number"

def test_registry_preserves_default_contracts() -> None:
    capability = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point="tests.capabilities.TestCapability",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,)
    )

    registered = registry.get(
        "test.capability"
    )

    assert registered.input_contract == "object"
    assert registered.output_contract == "object"