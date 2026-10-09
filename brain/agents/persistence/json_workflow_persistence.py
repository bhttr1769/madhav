
import hashlib
import json
import tempfile
from pathlib import Path

from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_persistence_state import (
    WorkflowPersistenceState,
)
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)


class JsonWorkflowPersistence:
    """Persist workflow and step snapshots as versioned JSON files."""

    _SCHEMA_VERSION = 1

    def __init__(self, storage_dir: str | Path) -> None:
        self._storage_dir = Path(storage_dir)

    def save(self, state: WorkflowPersistenceState) -> None:
        if not isinstance(state, WorkflowPersistenceState):
            raise TypeError(
                "state must be a WorkflowPersistenceState"
            )

        workflow = state.workflow
        payload = {
            "schema_version": self._SCHEMA_VERSION,
            "workflow": {
                "id": workflow.id,
                "goal_id": workflow.goal_id,
                "step_ids": list(workflow.step_ids),
                "status": workflow.status.value,
            },
            "steps": [
                {
                    "id": step.id,
                    "task_id": step.task_id,
                    "status": step.status.value,
                }
                for step in state.steps
            ],
        }

        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._path_for(workflow.id)
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

    def load(self, workflow_id: str) -> WorkflowPersistenceState:
        if not isinstance(workflow_id, str):
            raise TypeError("workflow_id must be a string")
        if not workflow_id.strip():
            raise ValueError("workflow_id must not be empty")

        path = self._path_for(workflow_id)

        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError:
            raise KeyError(workflow_id) from None
        except json.JSONDecodeError as exc:
            raise ValueError(
                "workflow persistence contains invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError("workflow persistence must be a JSON object")
        if payload.get("schema_version") != self._SCHEMA_VERSION:
            raise ValueError("unsupported workflow schema version")

        try:
            data = payload["workflow"]
            if not isinstance(data, dict):
                raise TypeError("workflow must be an object")
            if data["id"] != workflow_id:
                raise ValueError("persisted workflow ID does not match")

            step_data = payload["steps"]
            if not isinstance(step_data, list):
                raise TypeError("steps must be a list")

            workflow = Workflow(
                id=data["id"],
                goal_id=data["goal_id"],
                step_ids=tuple(data["step_ids"]),
                status=WorkflowStatus(data["status"]),
            )

            steps = tuple(
                WorkflowStep(
                    id=item["id"],
                    task_id=item["task_id"],
                    status=WorkflowStepStatus(item["status"]),
                )
                for item in step_data
            )

            return WorkflowPersistenceState(
                workflow=workflow,
                steps=steps,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "workflow persistence contains invalid state"
            ) from exc

    def _path_for(self, workflow_id: str) -> Path:
        digest = hashlib.sha256(
            workflow_id.encode("utf-8")
        ).hexdigest()
        return self._storage_dir / f"workflow-{digest}.json"
