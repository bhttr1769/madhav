import hashlib
import json
import tempfile
from pathlib import Path

from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)
from brain.agents.persistence.agent_operation_persistence import (
    AgentOperationPersistence,
)


class JsonAgentOperationPersistence(AgentOperationPersistence):
    """Persist operation checkpoints as individual JSON files."""

    _SCHEMA_VERSION = 1

    def __init__(self, storage_dir: str | Path) -> None:
        self._storage_dir = Path(storage_dir)

    def save(self, state: AgentOperationCheckpointState) -> None:
        if not isinstance(state, AgentOperationCheckpointState):
            raise TypeError(
                "state must be an AgentOperationCheckpointState"
            )

        operation = state.operation
        self._storage_dir.mkdir(parents=True, exist_ok=True)

        path = self._path_for(operation.id)
        payload = {
            "schema_version": self._SCHEMA_VERSION,
            "operation": {
                "id": operation.id,
                "goal_id": operation.goal_id,
                "workflow_id": operation.workflow_id,
                "status": operation.status.value,
            },
        }

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

    def load(
        self,
        operation_id: str,
    ) -> AgentOperationCheckpointState:
        if not isinstance(operation_id, str):
            raise TypeError("operation_id must be a string")

        if not operation_id.strip():
            raise ValueError("operation_id must not be empty")

        path = self._path_for(operation_id)

        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError:
            raise KeyError(operation_id) from None
        except json.JSONDecodeError as exc:
            raise ValueError(
                "operation checkpoint contains invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError("operation checkpoint must be a JSON object")

        if payload.get("schema_version") != self._SCHEMA_VERSION:
            raise ValueError("unsupported operation checkpoint schema version")

        data = payload.get("operation")
        if not isinstance(data, dict):
            raise ValueError("checkpoint operation must be a JSON object")

        if data.get("id") != operation_id:
            raise ValueError("checkpoint operation ID does not match")

        try:
            operation = AgentOperation(
                id=data["id"],
                goal_id=data["goal_id"],
                workflow_id=data["workflow_id"],
                status=AgentOperationStatus(data["status"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "operation checkpoint contains invalid operation data"
            ) from exc

        return AgentOperationCheckpointState(operation=operation)

    def _path_for(self, operation_id: str) -> Path:
        digest = hashlib.sha256(operation_id.encode("utf-8")).hexdigest()
        return self._storage_dir / f"operation-{digest}.json"