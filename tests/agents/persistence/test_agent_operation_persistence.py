import pytest

from brain.agents.models.agent_operation import AgentOperation
from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)
from brain.agents.persistence.agent_operation_persistence import (
    AgentOperationPersistence,
)


class FakeAgentOperationPersistence(AgentOperationPersistence):
    def __init__(self) -> None:
        self._states: dict[str, AgentOperationCheckpointState] = {}

    def save(self, state: AgentOperationCheckpointState) -> None:
        self._states[state.operation.id] = state

    def load(self, operation_id: str) -> AgentOperationCheckpointState:
        try:
            return self._states[operation_id]
        except KeyError:
            raise KeyError(operation_id) from None


def create_state() -> AgentOperationCheckpointState:
    return AgentOperationCheckpointState(
        operation=AgentOperation(
            id="operation-1",
            goal_id="goal-1",
            workflow_id="workflow-1",
        )
    )


def test_persistence_contract_can_be_implemented() -> None:
    assert isinstance(
        FakeAgentOperationPersistence(),
        AgentOperationPersistence,
    )


def test_save_and_load_operation_checkpoint() -> None:
    persistence = FakeAgentOperationPersistence()
    state = create_state()

    persistence.save(state)

    assert persistence.load("operation-1") is state


def test_load_rejects_unknown_operation() -> None:
    persistence = FakeAgentOperationPersistence()

    with pytest.raises(KeyError):
        persistence.load("unknown-operation")


def test_save_rejects_invalid_state() -> None:
    persistence = FakeAgentOperationPersistence()

    with pytest.raises(AttributeError):
        persistence.save(object())