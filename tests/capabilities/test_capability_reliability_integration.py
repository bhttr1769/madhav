from brain.capabilities.capability_reliability_assessor import (
    CapabilityReliabilityAssessor,
)
from brain.capabilities.capability_reliability_composer import (
    CapabilityReliabilityComposer,
)
from brain.capabilities.capability_runtime_verifier import (
    CapabilityRuntimeVerifier,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


def test_successful_capability_reliability_flow():
    execution = CapabilityExecutionResult(
        capability_id="test.capability",
        output={"result": "complete"},
    )

    verifier = CapabilityRuntimeVerifier()
    verification = verifier.verify(execution)

    assert verification.status == "verified"
    assert verification.passed is True

    assessor = CapabilityReliabilityAssessor()
    assessment = assessor.assess(
        execution,
        verification,
    )

    assert assessment.status == "reliable"

    composition = CapabilityComposition(
        id="test.composition",
        name="Test Composition",
        description="Test capability composition",
        version="1.0",
        capabilities=(
            CapabilityDescriptor(
                id="test.capability",
                name="Test Capability",
                description="Test capability",
                version="1.0",
                entry_point="test.module:TestCapability",
                dependencies=frozenset(),
            ),
        ),
    )

    composer = CapabilityReliabilityComposer()

    result = composer.compose(
        composition,
        (assessment,),
    )

    assert result.composition is composition
    assert result.assessments == (assessment,)

def test_failed_capability_reliability_flow():
    execution = CapabilityExecutionResult(
        capability_id="test.capability",
        output=None,
        status="failed",
        error=RuntimeError("execution failed"),
    )

    verifier = CapabilityRuntimeVerifier()
    verification = verifier.verify(execution)

    assert verification.status == "failed"
    assert verification.passed is False

    assessor = CapabilityReliabilityAssessor()
    assessment = assessor.assess(
        execution,
        verification,
    )

    assert assessment.status == "unreliable"