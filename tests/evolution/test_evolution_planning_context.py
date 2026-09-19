import pytest

from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.models.evolution_planning_context import (
    EvolutionPlanningContext,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


def create_request():
    return EvolutionRequest(
        requested_capability="repository_analysis",
        objective="Analyze a software repository.",
        constraints=frozenset(),
        mode="proposal",
    )


def create_assessment():
    return CapabilityAssessment(
        requested_capability="repository_analysis",
        available=False,
        status="unavailable",
        matched_capabilities=frozenset(),
        missing_capabilities=frozenset(
            {"repository_analysis"}
        ),
        rationale="Capability is not registered.",
    )


def create_capability():
    return CapabilityDescriptor(
        id="file_read",
        name="File Read",
        description="Reads files.",
        version="1.0.0",
        entry_point="brain.file_read.FileRead",
        dependencies=frozenset(),
    )


def test_creates_evolution_planning_context():
    request = create_request()
    assessment = create_assessment()
    capability = create_capability()

    context = EvolutionPlanningContext(
        request=request,
        assessment=assessment,
        available_capabilities=(
            capability,
        ),
    )

    assert context.request == request
    assert context.assessment == assessment
    assert context.available_capabilities == (
        capability,
    )


def test_planning_context_is_immutable():
    context = EvolutionPlanningContext(
        request=create_request(),
        assessment=create_assessment(),
        available_capabilities=(
            create_capability(),
        ),
    )

    with pytest.raises(
        AttributeError,
    ):
        context.request = create_request()