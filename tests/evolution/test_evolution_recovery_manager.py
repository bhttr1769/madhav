import pytest

from brain.evolution.evolution_recovery_manager import (
    EvolutionRecoveryManager,
)
from brain.evolution.models.evolution_recovery import EvolutionRecovery


def test_recovery_records_failed_evolution():
    manager = EvolutionRecoveryManager()

    recovery = manager.recover(
        evolution_id="evo-001",
        reason="engineering loop failed",
    )

    assert isinstance(recovery, EvolutionRecovery)
    assert recovery.evolution_id == "evo-001"
    assert recovery.recovered is False
    assert recovery.recovery_reason == "engineering loop failed"


def test_recovery_requires_evolution_id():
    manager = EvolutionRecoveryManager()

    with pytest.raises(ValueError):
        manager.recover(
            evolution_id="",
            reason="engineering loop failed",
        )


def test_recovery_requires_reason():
    manager = EvolutionRecoveryManager()

    with pytest.raises(ValueError):
        manager.recover(
            evolution_id="evo-001",
            reason="",
        )


def test_recovery_requires_string_evolution_id():
    manager = EvolutionRecoveryManager()

    with pytest.raises(TypeError):
        manager.recover(
            evolution_id=123,
            reason="engineering loop failed",
        )


def test_recovery_requires_string_reason():
    manager = EvolutionRecoveryManager()

    with pytest.raises(TypeError):
        manager.recover(
            evolution_id="evo-001",
            reason=123,
        )