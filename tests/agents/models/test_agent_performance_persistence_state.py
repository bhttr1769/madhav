from dataclasses import FrozenInstanceError

import pytest

from brain.agents.models.agent_performance_persistence_state import (
    AgentPerformancePersistenceState,
)
from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)


def create_record(agent_id="agent-1"):
    return AgentPerformanceRecord(
        agent_id=agent_id,
        total_evaluations=10,
        successful_outcomes=8,
        unsuccessful_outcomes=1,
        inconclusive_outcomes=1,
        verified_successes=8,
        verified_failures=1,
    )


def test_persistence_state_stores_agent_and_record():
    record = create_record()

    state = AgentPerformancePersistenceState(
        agent_id="agent-1",
        record=record,
    )

    assert state.agent_id == "agent-1"
    assert state.record is record


def test_persistence_state_is_immutable():
    state = AgentPerformancePersistenceState(
        agent_id="agent-1",
        record=create_record(),
    )

    with pytest.raises(FrozenInstanceError):
        state.agent_id = "agent-2"


def test_persistence_state_requires_string_agent_id():
    with pytest.raises(TypeError):
        AgentPerformancePersistenceState(
            agent_id=123,
            record=create_record(),
        )


def test_persistence_state_rejects_empty_agent_id():
    with pytest.raises(ValueError):
        AgentPerformancePersistenceState(
            agent_id="",
            record=create_record(),
        )


def test_persistence_state_requires_performance_record():
    with pytest.raises(TypeError):
        AgentPerformancePersistenceState(
            agent_id="agent-1",
            record=object(),
        )


def test_persistence_state_requires_matching_agent_id():
    record = create_record(agent_id="agent-2")

    with pytest.raises(
        ValueError,
        match="agent_id must match",
    ):
        AgentPerformancePersistenceState(
            agent_id="agent-1",
            record=record,
        )


def test_persistence_state_accepts_empty_performance_record():
    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    state = AgentPerformancePersistenceState(
        agent_id="agent-1",
        record=record,
    )

    assert state.record.total_evaluations == 0