import pytest

from brain.evolution.evolution_integration_recovery import (
    EvolutionIntegrationRecoveryManager,
)
from brain.evolution.models.evolution_integration_recovery import (
    EvolutionIntegrationRecovery,
)


def test_successful_integration_does_not_require_rollback():
    manager = EvolutionIntegrationRecoveryManager()

    recovery = manager.recover(
        evolution_id="evo-001",
        integration_succeeded=True,
        reason="capability integrated successfully",
    )

    assert isinstance(
        recovery,
        EvolutionIntegrationRecovery,
    )
    assert recovery.evolution_id == "evo-001"
    assert recovery.integration_succeeded is True
    assert recovery.rollback_required is False
    assert recovery.reason == (
        "capability integrated successfully"
    )


def test_failed_integration_requires_rollback():
    manager = EvolutionIntegrationRecoveryManager()

    recovery = manager.recover(
        evolution_id="evo-002",
        integration_succeeded=False,
        reason="capability integration failed",
    )

    assert recovery.integration_succeeded is False
    assert recovery.rollback_required is True
    assert recovery.reason == (
        "capability integration failed"
    )


def test_requires_evolution_id():
    manager = EvolutionIntegrationRecoveryManager()

    with pytest.raises(ValueError):
        manager.recover(
            evolution_id="",
            integration_succeeded=False,
            reason="integration failed",
        )


def test_requires_string_evolution_id():
    manager = EvolutionIntegrationRecoveryManager()

    with pytest.raises(TypeError):
        manager.recover(
            evolution_id=123,
            integration_succeeded=False,
            reason="integration failed",
        )


def test_requires_boolean_integration_result():
    manager = EvolutionIntegrationRecoveryManager()

    with pytest.raises(TypeError):
        manager.recover(
            evolution_id="evo-003",
            integration_succeeded="false",
            reason="integration failed",
        )


def test_requires_string_reason():
    manager = EvolutionIntegrationRecoveryManager()

    with pytest.raises(TypeError):
        manager.recover(
            evolution_id="evo-004",
            integration_succeeded=False,
            reason=123,
        )


def test_requires_non_empty_reason():
    manager = EvolutionIntegrationRecoveryManager()

    with pytest.raises(ValueError):
        manager.recover(
            evolution_id="evo-005",
            integration_succeeded=False,
            reason="",
        )