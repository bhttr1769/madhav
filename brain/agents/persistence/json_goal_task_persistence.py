
import hashlib
import json
import tempfile
from pathlib import Path

from brain.agents.goal_task_persistence import GoalTaskPersistence
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.goal_task_persistence_state import (
    GoalTaskPersistenceState,
)


class JsonGoalTaskPersistence:
    """Persist goal/task snapshots as versioned JSON files."""

    _SCHEMA_VERSION = 1

    def __init__(self, storage_dir: str | Path) -> None:
        self._storage_dir = Path(storage_dir)

    def save(self, state: GoalTaskPersistenceState) -> None:
        if not isinstance(state, GoalTaskPersistenceState):
            raise TypeError(
                "state must be a GoalTaskPersistenceState"
            )

        payload = {
            "schema_version": self._SCHEMA_VERSION,
            "agent_id": state.agent_id,
            "goals": [
                {
                    "id": goal.id,
                    "agent_id": goal.agent_id,
                    "description": goal.description,
                    "status": goal.status.value,
                    "progress": goal.progress,
                }
                for goal in state.goals
            ],
            "tasks": [
                {
                    "id": task.id,
                    "goal_id": task.goal_id,
                    "description": task.description,
                    "parent_task_id": task.parent_task_id,
                    "dependencies": sorted(task.dependencies),
                    "status": task.status.value,
                    "progress": task.progress,
                }
                for task in state.tasks
            ],
        }

        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._path_for(state.agent_id)
        temporary_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._storage_dir,
                suffix=".tmp",
                delete=False,
            ) as file:
                temporary_path = Path(file.name)
                json.dump(payload, file, indent=2)
                file.flush()

            temporary_path.replace(path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    def load(self, agent_id: str) -> GoalTaskPersistenceState:
        if not isinstance(agent_id, str):
            raise TypeError("agent_id must be a string")
        if not agent_id.strip():
            raise ValueError("agent_id must not be empty")

        path = self._path_for(agent_id)

        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError:
            raise KeyError(agent_id) from None
        except json.JSONDecodeError as exc:
            raise ValueError(
                "goal/task persistence contains invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError("goal/task persistence must be a JSON object")
        if payload.get("schema_version") != self._SCHEMA_VERSION:
            raise ValueError("unsupported goal/task schema version")
        if payload.get("agent_id") != agent_id:
            raise ValueError("persisted agent ID does not match")

        try:
            goals_data = payload["goals"]
            tasks_data = payload["tasks"]

            if not isinstance(goals_data, list):
                raise TypeError("goals must be a list")
            if not isinstance(tasks_data, list):
                raise TypeError("tasks must be a list")

            goals = tuple(
                Goal(
                    id=item["id"],
                    agent_id=item["agent_id"],
                    description=item["description"],
                    status=GoalStatus(item["status"]),
                    progress=item["progress"],
                )
                for item in goals_data
            )

            tasks = tuple(
                AgentTask(
                    id=item["id"],
                    goal_id=item["goal_id"],
                    description=item["description"],
                    parent_task_id=item["parent_task_id"],
                    dependencies=frozenset(item["dependencies"]),
                    status=AgentTaskStatus(item["status"]),
                    progress=item["progress"],
                )
                for item in tasks_data
            )

            return GoalTaskPersistenceState(
                agent_id=agent_id,
                goals=goals,
                tasks=tasks,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "goal/task persistence contains invalid state"
            ) from exc

    def _path_for(self, agent_id: str) -> Path:
        digest = hashlib.sha256(
            agent_id.encode("utf-8")
        ).hexdigest()
        return self._storage_dir / f"agent-{digest}.json"
