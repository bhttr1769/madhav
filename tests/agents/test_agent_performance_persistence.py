from brain.agents.agent_performance_persistence import (
    AgentPerformancePersistence,
)
from brain.agents.models.agent_performance_persistence_state import (
    AgentPerformancePersistenceState,
)
from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)


class FakeAgentPerformancePersistence:
    def __init__(self):
        self.saved_state = None

    def save(
        self,
        state: AgentPerformancePersistenceState,
    ) -> None:
        self.saved_state = state

    def load(
        self,
        agent_id: str,
    ) -> AgentPerformancePersistenceState:
        return self.saved_state


def test_persistence_contract_can_be_implemented():
    persistence = FakeAgentPerformancePersistence()

    assert isinstance(
        persistence,
        AgentPerformancePersistence,
    )


def test_persistence_contract_preserves_performance_state():
    persistence = FakeAgentPerformancePersistence()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
        total_evaluations=5,
        successful_outcomes=4,
        unsuccessful_outcomes=1,
        verified_successes=4,
        verified_failures=1,
    )

    state = AgentPerformancePersistenceState(
        agent_id="agent-1",
        record=record,
    )

    persistence.save(state)

    loaded = persistence.load("agent-1")

    assert loaded is state
    assert loaded.agent_id == "agent-1"
    assert loaded.record == record