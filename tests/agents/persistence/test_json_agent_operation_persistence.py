import json

import pytest

from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)
from brain.agents.persistence.json_agent_operation_persistence import (
    JsonAgentOperationPersistence,
)


@pytest.fixture
def persistence(tmp_path):
    return JsonAgentOperationPersistence(tmp_path / "operations")


@pytest.fixture
def state():
    return AgentOperationCheckpointState(
        operation=AgentOperation(
            id="operation-1",
            goal_id="goal-1",
            workflow_id="workflow-1",
            status=AgentOperationStatus.PAUSED,
        )
    )


def test_save_and_load_round_trip(persistence, state):
    persistence.save(state)

    restored = persistence.load("operation-1")

    assert restored == state
    assert restored.operation.status is AgentOperationStatus.PAUSED


def test_load_unknown_operation_raises_key_error(persistence):
    with pytest.raises(KeyError):
        persistence.load("missing-operation")


def test_save_rejects_invalid_state(persistence):
    with pytest.raises(TypeError, match="AgentOperationCheckpointState"):
        persistence.save(object())


def test_load_rejects_invalid_json(persistence, state):
    persistence.save(state)
    path = persistence._path_for("operation-1")
    path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON"):
        persistence.load("operation-1")


def test_load_rejects_mismatched_operation_id(persistence, state):
    persistence.save(state)
    path = persistence._path_for("operation-1")

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["operation"]["id"] = "another-operation"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="ID does not match"):
        persistence.load("operation-1")


def test_load_rejects_unknown_status(persistence, state):
    persistence.save(state)
    path = persistence._path_for("operation-1")

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["operation"]["status"] = "unknown"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid operation data"):
        persistence.load("operation-1")