
import hashlib
import json
import tempfile
from pathlib import Path
from threading import RLock

from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.remote_execution_record import (
    RemoteExecutionRecord,
    RemoteExecutionStatus,
)
from brain.agents.persistence.remote_execution_persistence import (
    RemoteExecutionPersistence,
)


class JsonRemoteExecutionPersistence(RemoteExecutionPersistence):
    """Persist remote execution records as versioned JSON files."""

    _SCHEMA_VERSION = 1

    _TRANSITIONS = {
        RemoteExecutionStatus.CLAIMED: {
            RemoteExecutionStatus.RUNNING,
            RemoteExecutionStatus.UNCERTAIN,
        },
        RemoteExecutionStatus.RUNNING: {
            RemoteExecutionStatus.COMPLETED,
            RemoteExecutionStatus.FAILED,
            RemoteExecutionStatus.UNCERTAIN,
        },
        RemoteExecutionStatus.COMPLETED: set(),
        RemoteExecutionStatus.FAILED: set(),
        RemoteExecutionStatus.UNCERTAIN: set(),
    }

    def __init__(self, storage_dir: str | Path) -> None:
        self._storage_dir = Path(storage_dir)
        self._lock = RLock()

    def claim(self, record: RemoteExecutionRecord) -> bool:
        if not isinstance(record, RemoteExecutionRecord):
            raise TypeError("record must be a RemoteExecutionRecord")
        if record.status is not RemoteExecutionStatus.CLAIMED:
            raise ValueError("new claims must have CLAIMED status")
        if record.response is not None:
            raise ValueError("new claims cannot contain a response")

        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._path_for(record.dispatch_id)
        payload = self._encode(record)

        # Exclusive creation is the claim boundary across processes.
        # If a process crashes while writing, load will fail closed.
        with self._lock:
            try:
                with path.open("x", encoding="utf-8") as file:
                    json.dump(payload, file, indent=2)
                    file.flush()
            except FileExistsError:
                return False

        return True

    def load(self, dispatch_id: str) -> RemoteExecutionRecord:
        self._validate_dispatch_id(dispatch_id)
        path = self._path_for(dispatch_id)

        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError:
            raise KeyError(dispatch_id) from None
        except json.JSONDecodeError as exc:
            raise ValueError(
                "remote execution record contains invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError(
                "remote execution record must be a JSON object"
            )
        if payload.get("schema_version") != self._SCHEMA_VERSION:
            raise ValueError(
                "unsupported remote execution record schema version"
            )
        if payload.get("dispatch_id") != dispatch_id:
            raise ValueError("persisted dispatch ID does not match")

        try:
            response_data = payload.get("response")
            response = None

            if response_data is not None:
                response = AgentMessage(
                    id=response_data["id"],
                    sender_agent_id=response_data["sender_agent_id"],
                    recipient_agent_id=response_data["recipient_agent_id"],
                    message_type=AgentMessageType(
                        response_data["message_type"]
                    ),
                    payload=response_data["payload"],
                    correlation_id=response_data["correlation_id"],
                )

            return RemoteExecutionRecord(
                dispatch_id=payload["dispatch_id"],
                request_fingerprint=payload["request_fingerprint"],
                owner_node_id=payload["owner_node_id"],
                status=RemoteExecutionStatus(payload["status"]),
                response=response,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "remote execution record contains invalid data"
            ) from exc

    def save(self, record: RemoteExecutionRecord) -> None:
        if not isinstance(record, RemoteExecutionRecord):
            raise TypeError("record must be a RemoteExecutionRecord")

        with self._lock:
            current = self.load(record.dispatch_id)

            if current.request_fingerprint != record.request_fingerprint:
                raise ValueError("dispatch request fingerprint cannot change")
            if current.owner_node_id != record.owner_node_id:
                raise ValueError("dispatch owner cannot change implicitly")

            allowed = self._TRANSITIONS[current.status]
            if record.status not in allowed:
                raise ValueError(
                    f"invalid remote execution transition: "
                    f"{current.status.value} -> {record.status.value}"
                )

            self._write_atomically(record)

    def all(self) -> tuple[RemoteExecutionRecord, ...]:
        if not self._storage_dir.exists():
            return ()

        records = []
        for path in sorted(
            self._storage_dir.glob("remote-execution-*.json")
        ):
            # Load through the normal validation path.
            payload_dispatch_id = self._read_dispatch_id(path)
            records.append(self.load(payload_dispatch_id))

        return tuple(records)

    def _write_atomically(self, record: RemoteExecutionRecord) -> None:
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._path_for(record.dispatch_id)
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
                json.dump(self._encode(record), file, indent=2)
                file.flush()

            temporary_path.replace(path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    @staticmethod
    def _encode(record: RemoteExecutionRecord) -> dict[str, object]:
        response = record.response
        response_data = None

        if response is not None:
            response_data = {
                "id": response.id,
                "sender_agent_id": response.sender_agent_id,
                "recipient_agent_id": response.recipient_agent_id,
                "message_type": response.message_type.value,
                "payload": response.payload,
                "correlation_id": response.correlation_id,
            }

        payload = {
            "schema_version": JsonRemoteExecutionPersistence._SCHEMA_VERSION,
            "dispatch_id": record.dispatch_id,
            "request_fingerprint": record.request_fingerprint,
            "owner_node_id": record.owner_node_id,
            "status": record.status.value,
            "response": response_data,
        }

        try:
            json.dumps(payload, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "remote execution record must be JSON-compatible"
            ) from exc

        return payload

    @staticmethod
    def _read_dispatch_id(path: Path) -> str:
        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(
                f"cannot read remote execution record: {path.name}"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError(
                f"invalid remote execution record: {path.name}"
            )

        dispatch_id = payload.get("dispatch_id")
        if not isinstance(dispatch_id, str) or not dispatch_id.strip():
            raise ValueError(
                f"invalid dispatch ID in record: {path.name}"
            )

        return dispatch_id

    def _path_for(self, dispatch_id: str) -> Path:
        digest = hashlib.sha256(dispatch_id.encode("utf-8")).hexdigest()
        return self._storage_dir / f"remote-execution-{digest}.json"

    @staticmethod
    def _validate_dispatch_id(dispatch_id: str) -> None:
        if not isinstance(dispatch_id, str):
            raise TypeError("dispatch_id must be a string")
        if not dispatch_id.strip():
            raise ValueError("dispatch_id must not be empty")
