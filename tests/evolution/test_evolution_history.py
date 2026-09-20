from datetime import datetime

from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)


def test_evolution_history_stores_run_information():
    started_at = datetime(
        2026,
        9,
        20,
        10,
        0,
    )

    completed_at = datetime(
        2026,
        9,
        20,
        10,
        5,
    )

    history = EvolutionHistory(
        evolution_id="evo-001",
        requested_capability="web_research",
        objective="Add web research capability.",
        mode="autonomous",
        status="completed",
        started_at=started_at,
        completed_at=completed_at,
        task_count=3,
        completed_task_count=3,
        passed=True,
        termination_reason="completed",
    )

    assert history.evolution_id == "evo-001"
    assert (
        history.requested_capability
        == "web_research"
    )
    assert (
        history.objective
        == "Add web research capability."
    )
    assert history.mode == "autonomous"
    assert history.status == "completed"
    assert history.started_at == started_at
    assert history.completed_at == completed_at
    assert history.task_count == 3
    assert history.completed_task_count == 3
    assert history.passed is True
    assert (
        history.termination_reason
        == "completed"
    )


def test_evolution_history_can_represent_running_evolution():
    started_at = datetime(
        2026,
        9,
        20,
        10,
        0,
    )

    history = EvolutionHistory(
        evolution_id="evo-002",
        requested_capability="code_analysis",
        objective="Add code analysis capability.",
        mode="supervised",
        status="running",
        started_at=started_at,
        completed_at=None,
        task_count=2,
        completed_task_count=0,
        passed=False,
        termination_reason="running",
    )

    assert history.status == "running"
    assert history.completed_at is None
    assert history.completed_task_count == 0
    assert history.passed is False