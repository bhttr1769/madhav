import pytest

from brain.capabilities.capability_integrator import (
    CapabilityIntegrator,
)
from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def _capability():
    return CapabilityDescriptor(
        id="web_research",
        name="Web Research",
        description="Research information from the web.",
        version="1.0.0",
        entry_point="brain.research:WebResearch",
        dependencies=frozenset(),
    )


def test_integrator_registers_verified_capability():
    registry = CapabilityRegistry()
    integrator = CapabilityIntegrator(registry)

    capability = _capability()

    integrator.integrate(
        capability=capability,
        verification_passed=True,
    )

    assert registry.has(
        "web_research"
    )

    assert registry.get(
        "web_research"
    ) == capability


def test_integrator_rejects_unverified_capability():
    registry = CapabilityRegistry()
    integrator = CapabilityIntegrator(registry)

    capability = _capability()

    with pytest.raises(
        ValueError,
        match="cannot integrate an unverified capability",
    ):
        integrator.integrate(
            capability=capability,
            verification_passed=False,
        )

    assert not registry.has(
        "web_research"
    )


def test_integrator_rejects_invalid_capability():
    registry = CapabilityRegistry()
    integrator = CapabilityIntegrator(registry)

    with pytest.raises(
        TypeError,
        match="capability must be a CapabilityDescriptor",
    ):
        integrator.integrate(
            capability="web_research",
            verification_passed=True,
        )


def test_integrator_rejects_invalid_verification_value():
    registry = CapabilityRegistry()
    integrator = CapabilityIntegrator(registry)

    with pytest.raises(
        TypeError,
        match="verification_passed must be a bool",
    ):
        integrator.integrate(
            capability=_capability(),
            verification_passed="true",
        )


def test_integrator_preserves_duplicate_registration_protection():
    registry = CapabilityRegistry()
    integrator = CapabilityIntegrator(registry)

    capability = _capability()

    integrator.integrate(
        capability=capability,
        verification_passed=True,
    )

    with pytest.raises(
        ValueError,
        match="capability already registered",
    ):
        integrator.integrate(
            capability=capability,
            verification_passed=True,
        )