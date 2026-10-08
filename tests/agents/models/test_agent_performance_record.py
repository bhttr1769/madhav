import pytest

from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)


def test_empty_record_is_valid():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    assert record.agent_id == "agent-1"
    assert record.total_evaluations == 0
    assert record.successful_outcomes == 0
    assert record.unsuccessful_outcomes == 0
    assert record.inconclusive_outcomes == 0
    assert record.verified_successes == 0
    assert record.verified_failures == 0
    assert record.reliability == 0.0


def test_record_accepts_valid_counts():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
        total_evaluations=10,
        successful_outcomes=7,
        unsuccessful_outcomes=2,
        inconclusive_outcomes=1,
        verified_successes=7,
        verified_failures=2,
    )

    assert record.total_evaluations == 10
    assert record.successful_outcomes == 7
    assert record.unsuccessful_outcomes == 2
    assert record.inconclusive_outcomes == 1
    assert record.verified_successes == 7
    assert record.verified_failures == 2


def test_reliability_uses_verified_results_only():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
        total_evaluations=15,
        successful_outcomes=8,
        unsuccessful_outcomes=2,
        inconclusive_outcomes=5,
        verified_successes=8,
        verified_failures=2,
    )

    assert record.reliability == 0.8


def test_inconclusive_results_are_not_failures():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
        total_evaluations=5,
        successful_outcomes=2,
        unsuccessful_outcomes=0,
        inconclusive_outcomes=3,
        verified_successes=2,
        verified_failures=0,
    )

    assert record.reliability == 1.0


def test_no_verified_results_has_zero_reliability():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
        total_evaluations=3,
        successful_outcomes=0,
        unsuccessful_outcomes=0,
        inconclusive_outcomes=3,
    )

    assert record.reliability == 0.0


def test_agent_id_must_be_string():
    with pytest.raises(TypeError):
        AgentPerformanceRecord(
            agent_id=123,
        )


def test_agent_id_must_not_be_empty():
    with pytest.raises(ValueError):
        AgentPerformanceRecord(
            agent_id="",
        )


def test_counts_must_be_integers():
    with pytest.raises(TypeError):
        AgentPerformanceRecord(
            agent_id="agent-1",
            total_evaluations=1.5,
        )


def test_bool_is_not_valid_count():
    with pytest.raises(TypeError):
        AgentPerformanceRecord(
            agent_id="agent-1",
            total_evaluations=True,
        )


def test_counts_must_not_be_negative():
    with pytest.raises(ValueError):
        AgentPerformanceRecord(
            agent_id="agent-1",
            total_evaluations=-1,
        )


def test_outcome_counts_must_match_total():
    with pytest.raises(ValueError):
        AgentPerformanceRecord(
            agent_id="agent-1",
            total_evaluations=5,
            successful_outcomes=3,
            unsuccessful_outcomes=1,
            inconclusive_outcomes=0,
        )


def test_verified_counts_cannot_exceed_total():
    with pytest.raises(ValueError):
        AgentPerformanceRecord(
            agent_id="agent-1",
            total_evaluations=2,
            successful_outcomes=1,
            unsuccessful_outcomes=1,
            inconclusive_outcomes=0,
            verified_successes=2,
            verified_failures=1,
        )


def test_record_is_immutable():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    with pytest.raises(AttributeError):
        record.agent_id = "agent-2"