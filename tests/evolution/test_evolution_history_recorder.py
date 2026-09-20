import pytest
from datetime import datetime

from brain.evolution.evolution_history_recorder import (
    EvolutionHistoryRecorder,
)
from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)


def _history(
    evolution_id="evo-001",
):
    return EvolutionHistory(
        evolution_id=evolution_id,
        requested_capability="web_research",
        objective="Add web research capability.",
        mode="supervised",
        status="completed",
        started_at=__import__(
            "datetime"
        ).datetime(2026, 9, 20, 10, 0),
        completed_at=__import__(
            "datetime"
        ).datetime(2026, 9, 20, 10, 0),
        task_count=1,
        completed_task_count=1,
        passed=True,
        termination_reason="completed",
    )


def test_recorder_stores_history():
    recorder = EvolutionHistoryRecorder()

    history = _history()

    recorder.record(history)

    assert recorder.all() == (
        history,
    )


def test_recorder_stores_multiple_history_records():
    recorder = EvolutionHistoryRecorder()

    first = _history("evo-001")
    second = _history("evo-002")

    recorder.record(first)
    recorder.record(second)

    assert recorder.all() == (
        first,
        second,
    )


def test_recorder_returns_history_by_id():
    recorder = EvolutionHistoryRecorder()

    history = _history()

    recorder.record(history)

    assert recorder.get(
        "evo-001"
    ) == history


def test_recorder_rejects_unknown_id():
    recorder = EvolutionHistoryRecorder()

    with pytest.raises(
        KeyError,
        match="evolution history not found",
    ):
        recorder.get("missing")


def test_recorder_rejects_invalid_history():
    recorder = EvolutionHistoryRecorder()

    with pytest.raises(
        TypeError,
        match="EvolutionHistory",
    ):
        recorder.record(object())


def test_recorder_rejects_invalid_id():
    recorder = EvolutionHistoryRecorder()

    with pytest.raises(
        TypeError,
        match="evolution_id must be a string",
    ):
        recorder.get(123)


def test_recorder_rejects_empty_id():
    recorder = EvolutionHistoryRecorder()

    with pytest.raises(
        ValueError,
        match="evolution_id must not be empty",
    ):
        recorder.get("")