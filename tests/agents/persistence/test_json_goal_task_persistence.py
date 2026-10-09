
import json

import pytest

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.goal_task_persistence_state import (
    GoalTaskPersistenceState,
)
from brain.agents.persistence.json_goal_task_persistence import (
    JsonGoalTaskPersistence,
)


def make_state(agent_id="agent-1"):
    goal = Goal(
        id="goal-1",
        agent_id=agent_id,
        description="Build a feature",
        status=GoalStatus.ACTIVE,
        progress=50,
    )
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Implement the feature",
        parent_task_id=None,
        dependencies=frozenset({"task-0"}),
        status=AgentTaskStatus.ACTIVE,
        progress=25,
    )
    return GoalTaskPersistenceState(
        agent_id=agent_id,
        goals=(goal,),
        tasks=(task,),
    )


def test_save_and_load_round_trip(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)
    state = make_state()

    persistence.save(state)
    restored = persistence.load("agent-1")

    assert restored == state


def test_load_from_new_instance(tmp_path):
    JsonGoalTaskPersistence(tmp_path).save(make_state())

    restored = JsonGoalTaskPersistence(tmp_path).load("agent-1")

    assert restored == make_state()


def test_unknown_agent_raises_key_error(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)

    with pytest.raises(KeyError):
        persistence.load("unknown-agent")


def test_invalid_agent_id_is_rejected(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)

    with pytest.raises((TypeError, ValueError)):
        persistence.load(" ")


def test_malformed_json_is_rejected(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)
    path = persistence._path_for("agent-1")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError):
        persistence.load("agent-1")


def test_unsupported_schema_version_is_rejected(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)
    path = persistence._path_for("agent-1")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 999,
                "agent_id": "agent-1",
                "goals": [],
                "tasks": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        persistence.load("agent-1")


def test_mismatched_agent_id_is_rejected(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)
    persistence.save(make_state("agent-1"))

    path = persistence._path_for("agent-1")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["agent_id"] = "agent-2"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        persistence.load("agent-1")


def test_invalid_goal_or_task_state_is_rejected(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)
    persistence.save(make_state())

    path = persistence._path_for("agent-1")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["goals"][0]["status"] = "not-a-valid-status"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        persistence.load("agent-1")


def test_save_rejects_wrong_state_type(tmp_path):
    persistence = JsonGoalTaskPersistence(tmp_path)

    with pytest.raises(TypeError):
        persistence.save(object())
