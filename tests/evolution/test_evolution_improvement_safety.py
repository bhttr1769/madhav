import pytest

from brain.evolution.models.evolution_discovery_request import (
    EvolutionDiscoveryRequest,
)

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from tests.evolution.test_evolution_executor import (
    AUTONOMOUS_VERIFICATION_COMMAND,
    EvolvedCapabilityProvider,
    FakeCapabilityDiscovery,
    _executor,
)

from tests.evolution.test_evolution_improvement_execution import (
    _plan,
)

from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)

from brain.evolution.models.evolution_validation_result import (
    EvolutionValidationResult,
)

class FakeFailedEvolutionValidator:
    def __init__(self):
        self.calls = []

    def validate(
        self,
        proposed_changes,
        engineering_result,
        capabilities,
        requested_capability,
        verification_command,
    ):
        self.calls.append(
            (
                proposed_changes,
                engineering_result,
                capabilities,
                requested_capability,
                verification_command,
            )
        )

        from brain.evolution.models.evolution_validation_check import (
            EvolutionValidationCheck,
        )
        from brain.evolution.models.evolution_validation_result import (
            EvolutionValidationResult,
        )

        return EvolutionValidationResult(
            checks=(
                EvolutionValidationCheck(
                    name="change_validation",
                    passed=False,
                    reason="improvement validation failed",
                ),
            ),
        )


def test_improvement_execution_reuses_existing_autonomous_safety_boundary():
    plan = _plan()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    with pytest.raises(
        TypeError,
        match=(
            "autonomous execution requires an "
            "EvolutionDiscoveryRequest"
        ),
    ):
        executor.execute_improvement(
            improvement_plan=plan,
            mode="autonomous",
        )


def test_improvement_execution_rejects_supervised_integration_request():
    plan = _plan()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        ValueError,
        match=(
            "integration_request is only valid "
            "for autonomous mode"
        ),
    ):
        executor.execute_improvement(
            improvement_plan=plan,
            mode="supervised",
            integration_request=discovery_request,
        )


def test_improvement_execution_preserves_improvement_category():
    plan = _plan()

    assert plan.proposal.category is (
        EvolutionImprovementCategory.VERIFICATION
    )

    assert plan.category is (
        EvolutionImprovementCategory.VERIFICATION
    )

def test_improvement_execution_propagates_engineering_failure():
    plan = _plan()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        engineering_loop_exception=RuntimeError(
            "engineering failed"
        )
    )

    with pytest.raises(
        RuntimeError,
        match="engineering failed",
    ):
        executor.execute_improvement(
            improvement_plan=plan,
        )

def test_improvement_execution_uses_existing_validation_boundary():
    plan = _plan()

    validator = FakeFailedEvolutionValidator()

    events = []

    discovery = FakeCapabilityDiscovery(
        (
            EvolvedCapabilityProvider.capability_descriptor(),
        )
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        discovery=discovery,
        evolution_validator=validator,
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "evolution validation failed: "
            "improvement validation failed"
        ),
    ):
        executor.execute_improvement(
            improvement_plan=plan,
            mode="autonomous",
            integration_request=discovery_request,
        )

    assert len(validator.calls) == 1

    (
        proposed_changes,
        engineering_result,
        capabilities,
        requested_capability,
        verification_command,
    ) = validator.calls[0]

    assert proposed_changes
    assert engineering_result is not None
    assert requested_capability == (
        "evolution_validator"
    )
    assert verification_command == (
        AUTONOMOUS_VERIFICATION_COMMAND
    )

    assert "commit" not in events
    assert "integration" not in events