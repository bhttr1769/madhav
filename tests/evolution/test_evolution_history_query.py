from datetime import datetime

import pytest

from brain.evolution.evolution_history_query import (
    EvolutionHistoryQuery,
)
from brain.evolution.evolution_history_recorder import (
    EvolutionHistoryRecorder,
)
from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)


def _history(
    evolution_id,
    capability,
    status,
    passed,
):
    return EvolutionHistory(
        evolution_id=evolution_id,
        requested_capability=capability,
        objective=f"Add {capability}.",
        mode="supervised",
        status=status,
        started_at=datetime(
            2026,
            9,
            20,
            10,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            20,
            10,
            5,
        ),
        task_count=1,
        completed_task_count=1,
        passed=passed,
        termination_reason=(
            "completed"
            if passed
            else "verification_failed"
        ),
    )


def _query():
    recorder = EvolutionHistoryRecorder()

    histories = (
        _history(
            "evo-001",
            "web_research",
            "completed",
            True,
        ),
        _history(
            "evo-002",
            "code_analysis",
            "failed",
            False,
        ),
        _history(
            "evo-003",
            "web_research",
            "failed",
            False,
        ),
    )

    for history in histories:
        recorder.record(history)

    return EvolutionHistoryQuery(
        recorder
    ), histories


def test_all_returns_all_history():
    query, histories = _query()

    assert query.all() == histories


def test_by_capability_filters_history():
    query, histories = _query()

    result = query.by_capability(
        "web_research"
    )

    assert result == (
        histories[0],
        histories[2],
    )


def test_by_status_filters_history():
    query, histories = _query()

    result = query.by_status(
        "failed"
    )

    assert result == (
        histories[1],
        histories[2],
    )


def test_passed_returns_successful_history():
    query, histories = _query()

    assert query.passed() == (
        histories[0],
    )


def test_failed_returns_unsuccessful_history():
    query, histories = _query()

    assert query.failed() == (
        histories[1],
        histories[2],
    )


def test_by_capability_rejects_invalid_value():
    query, _ = _query()

    with pytest.raises(
        TypeError,
        match="requested_capability must be a string",
    ):
        query.by_capability(123)


def test_by_capability_rejects_empty_value():
    query, _ = _query()

    with pytest.raises(
        ValueError,
        match="requested_capability must not be empty",
    ):
        query.by_capability("")


def test_by_status_rejects_invalid_value():
    query, _ = _query()

    with pytest.raises(
        TypeError,
        match="status must be a string",
    ):
        query.by_status(123)


def test_by_status_rejects_empty_value():
    query, _ = _query()

    with pytest.raises(
        ValueError,
        match="status must not be empty",
    ):
        query.by_status("")