import json
from dataclasses import fields, is_dataclass
from enum import Enum
from threading import Event, RLock
from typing import Mapping
from uuid import uuid4

from brain.agents.agent_runtime import AgentRuntime
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
from brain.safety.logging.models.action_log_event import ActionLogEvent
from brain.safety.logging.models.action_log_status import ActionLogStatus
from brain.safety.logging.services.logging_service import LoggingService
from brain.safety.models.action import Action


class RemoteExecutionUncertainError(RuntimeError):
    """A dispatch cannot safely be re-executed automatically."""


class _ExecutionEntry:
    def __init__(self, fingerprint: str) -> None:
        self.fingerprint = fingerprint
        self.completed = Event()
        self.response: AgentMessage | None = None
        self.error: Exception | None = None


class RemoteTaskExecutionHandler:
    """Execute remote capabilities with optional durable idempotency."""

    def __init__(
        self,
        persistence: RemoteExecutionPersistence | None = None,
        owner_node_id: str = "local",
        logging_service: LoggingService | None = None,
    ) -> None:
        if persistence is not None and not isinstance(
            persistence,
            RemoteExecutionPersistence,
        ):
            raise TypeError(
                "persistence must be a RemoteExecutionPersistence or None"
            )

        if not isinstance(owner_node_id, str):
            raise TypeError("owner_node_id must be a string")
        if not owner_node_id.strip():
            raise ValueError("owner_node_id must not be empty")

        if logging_service is not None and not isinstance(
            logging_service,
            LoggingService,
        ):
            raise TypeError(
                "logging_service must be a LoggingService or None"
            )

        self._persistence = persistence
        self._owner_node_id = owner_node_id
        self._logging_service = logging_service
        self._entries: dict[str, _ExecutionEntry] = {}
        self._lock = RLock()

    def handle(
        self,
        message: AgentMessage,
        runtime: AgentRuntime,
        *,
        authority_agent_id: str | None = None,
    ) -> AgentMessage:
        if not isinstance(message, AgentMessage):
            raise TypeError("message must be an AgentMessage")
        if not isinstance(runtime, AgentRuntime):
            raise TypeError("runtime must be an AgentRuntime")

        if authority_agent_id is not None:
            if not isinstance(authority_agent_id, str):
                raise TypeError("authority_agent_id must be a string")
            if not authority_agent_id.strip():
                raise ValueError("authority_agent_id must not be empty")
            if authority_agent_id != message.sender_agent_id:
                raise ValueError(
                    "authority agent must match the requesting agent"
                )

        payload = message.payload
        if message.message_type != AgentMessageType.REQUEST:
            raise ValueError("remote task message must be a REQUEST")
        if payload.get("kind") != "remote_task_dispatch":
            raise ValueError("unsupported remote task message kind")

        dispatch_id = payload.get("dispatch_id")
        capability_id = payload.get("capability_id")
        self._require_string(dispatch_id, "dispatch_id")
        self._require_string(capability_id, "capability_id")

        if message.correlation_id != dispatch_id:
            raise ValueError(
                "message correlation ID does not match dispatch ID"
            )
        if message.recipient_agent_id != runtime.agent_id:
            raise ValueError(
                "message recipient does not match runtime agent"
            )

        fingerprint = self._fingerprint(message)

        with self._lock:
            entry = self._entries.get(dispatch_id)
            if entry is None:
                entry = _ExecutionEntry(fingerprint)
                self._entries[dispatch_id] = entry
                is_owner = True
            else:
                if entry.fingerprint != fingerprint:
                    raise ValueError(
                        "dispatch ID was reused with a different request"
                    )
                is_owner = False

        if not is_owner:
            entry.completed.wait()

            if entry.error is not None:
                self._log(
                    message,
                    ActionLogEvent.EXECUTION_FAILED,
                    ActionLogStatus.FAILED,
                    phase="result_reuse",
                    outcome="uncertain",
                    error_type=type(entry.error).__name__,
                )
                raise RemoteExecutionUncertainError(
                    f"dispatch {dispatch_id} did not produce a reusable result"
                ) from entry.error

            if entry.response is None:
                self._log(
                    message,
                    ActionLogEvent.EXECUTION_FAILED,
                    ActionLogStatus.FAILED,
                    phase="result_reuse",
                    outcome="uncertain",
                    error_type="MissingExecutionResponse",
                )
                raise RuntimeError(
                    "execution finished without a recorded response"
                )

            self._log_response(
                message,
                entry.response,
                phase="result_reuse",
                outcome="cached_result_reused",
            )
            return entry.response

        execution_started = False

        try:
            if self._persistence is not None:
                cached = self._claim_or_reuse(message, fingerprint)
                if cached is not None:
                    entry.response = cached
                    self._log_response(
                        message,
                        cached,
                        phase="durable_result_reuse",
                        outcome="cached_result_reused",
                    )
                    return cached

                self._persistence.save(
                    RemoteExecutionRecord(
                        dispatch_id=dispatch_id,
                        request_fingerprint=fingerprint,
                        owner_node_id=self._owner_node_id,
                        status=RemoteExecutionStatus.RUNNING,
                    )
                )

            input_data = payload.get(
                "input_payload",
                payload.get("input"),
            )

            self._log(
                message,
                ActionLogEvent.EXECUTION_STARTED,
                ActionLogStatus.RUNNING,
                phase="remote_execution",
                outcome="started",
            )
            execution_started = True

            try:
                if authority_agent_id is None:
                    output = runtime.execute_capability(
                        capability_id,
                        input_data,
                    )
                else:
                    output = runtime.execute_capability(
                        capability_id,
                        input_data,
                        authority_agent_id=authority_agent_id,
                    )
            except Exception as exc:
                response = self._build_response(
                    message,
                    status="failed",
                    output=None,
                    error=f"{type(exc).__name__}: {exc}",
                )
                self._persist_terminal(
                    dispatch_id,
                    fingerprint,
                    RemoteExecutionStatus.FAILED,
                    response,
                )
                entry.response = response
                self._log_response(
                    message,
                    response,
                    phase="remote_execution",
                    outcome="failed",
                    error_type=type(exc).__name__,
                )
                return response

            try:
                safe_output = self._to_json_value(output)
                response = self._build_response(
                    message,
                    status="completed",
                    output=safe_output,
                    error=None,
                )
            except Exception as exc:
                self._persist_uncertain(dispatch_id, fingerprint)
                raise RemoteExecutionUncertainError(
                    "capability returned an outcome that could not be "
                    "safely recorded; automatic retry is unsafe"
                ) from exc

            self._persist_terminal(
                dispatch_id,
                fingerprint,
                RemoteExecutionStatus.COMPLETED,
                response,
            )
            entry.response = response
            self._log_response(
                message,
                response,
                phase="remote_execution",
                outcome="completed",
            )
            return response

        except Exception as exc:
            entry.error = exc

            if execution_started or isinstance(
                exc,
                RemoteExecutionUncertainError,
            ):
                self._log(
                    message,
                    ActionLogEvent.EXECUTION_FAILED,
                    ActionLogStatus.FAILED,
                    phase="remote_execution",
                    outcome="uncertain",
                    error_type=type(exc).__name__,
                )

            raise
        finally:
            entry.completed.set()

    def _claim_or_reuse(
        self,
        message: AgentMessage,
        fingerprint: str,
    ) -> AgentMessage | None:
        dispatch_id = message.payload["dispatch_id"]
        record = RemoteExecutionRecord(
            dispatch_id=dispatch_id,
            request_fingerprint=fingerprint,
            owner_node_id=self._owner_node_id,
            status=RemoteExecutionStatus.CLAIMED,
        )

        assert self._persistence is not None

        if self._persistence.claim(record):
            return None

        existing = self._persistence.load(dispatch_id)

        if existing.request_fingerprint != fingerprint:
            raise ValueError(
                "dispatch ID was reused with a different request"
            )

        if existing.status in {
            RemoteExecutionStatus.COMPLETED,
            RemoteExecutionStatus.FAILED,
        }:
            if existing.response is None:
                raise ValueError(
                    "terminal dispatch record has no response"
                )
            return existing.response

        if existing.owner_node_id != self._owner_node_id:
            raise RemoteExecutionUncertainError(
                f"dispatch is owned by node {existing.owner_node_id}; "
                "ownership transfer requires explicit reconciliation"
            )

        raise RemoteExecutionUncertainError(
            f"dispatch {dispatch_id} is already "
            f"{existing.status.value}; refusing automatic re-execution"
        )

    def _persist_terminal(
        self,
        dispatch_id: str,
        fingerprint: str,
        status: RemoteExecutionStatus,
        response: AgentMessage,
    ) -> None:
        if self._persistence is None:
            return

        self._persistence.save(
            RemoteExecutionRecord(
                dispatch_id=dispatch_id,
                request_fingerprint=fingerprint,
                owner_node_id=self._owner_node_id,
                status=status,
                response=response,
            )
        )

    def _persist_uncertain(
        self,
        dispatch_id: str,
        fingerprint: str,
    ) -> None:
        if self._persistence is None:
            return

        self._persistence.save(
            RemoteExecutionRecord(
                dispatch_id=dispatch_id,
                request_fingerprint=fingerprint,
                owner_node_id=self._owner_node_id,
                status=RemoteExecutionStatus.UNCERTAIN,
            )
        )

    @staticmethod
    def _build_response(
        message: AgentMessage,
        status: str,
        output: object,
        error: str | None,
    ) -> AgentMessage:
        request = message.payload
        response_payload: dict[str, object] = {
            "kind": "remote_task_result",
            "dispatch_id": request["dispatch_id"],
            "task_id": request["task_id"],
            "goal_id": request["goal_id"],
            "workflow_id": request["workflow_id"],
            "workflow_step_id": request.get(
                "workflow_step_id",
                request.get("step_id"),
            ),
            "operation_id": request["operation_id"],
            "status": status,
            "output": output,
            "error": error,
        }

        return AgentMessage(
            id=str(uuid4()),
            sender_agent_id=message.recipient_agent_id,
            recipient_agent_id=message.sender_agent_id,
            message_type=AgentMessageType.RESPONSE,
            payload=response_payload,
            correlation_id=message.correlation_id,
        )

    @staticmethod
    def _fingerprint(message: AgentMessage) -> str:
        canonical = {
            "sender_agent_id": message.sender_agent_id,
            "recipient_agent_id": message.recipient_agent_id,
            "correlation_id": message.correlation_id,
            "payload": message.payload,
        }
        try:
            return json.dumps(
                canonical,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "remote task request must contain JSON-compatible data"
            ) from exc

    @classmethod
    def _to_json_value(cls, value: object) -> object:
        if value is None or isinstance(value, (str, int, bool)):
            return value

        if isinstance(value, float):
            if value != value or value in (
                float("inf"),
                float("-inf"),
            ):
                raise ValueError("non-finite floats cannot be returned")
            return value

        if isinstance(value, Enum):
            return cls._to_json_value(value.value)

        if is_dataclass(value) and not isinstance(value, type):
            return {
                field.name: cls._to_json_value(
                    getattr(value, field.name)
                )
                for field in fields(value)
            }

        if isinstance(value, Mapping):
            if not all(isinstance(key, str) for key in value):
                raise TypeError("result mapping keys must be strings")
            return {
                key: cls._to_json_value(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [cls._to_json_value(item) for item in value]

        raise TypeError(
            f"unsupported capability result type: {type(value).__name__}"
        )

    def _log_response(
        self,
        message: AgentMessage,
        response: AgentMessage,
        *,
        phase: str,
        outcome: str,
        error_type: str | None = None,
    ) -> None:
        if response.payload.get("status") == "completed":
            event = ActionLogEvent.EXECUTION_COMPLETED
            status = ActionLogStatus.COMPLETED
        else:
            event = ActionLogEvent.EXECUTION_FAILED
            status = ActionLogStatus.FAILED

        self._log(
            message,
            event,
            status,
            phase=phase,
            outcome=outcome,
            error_type=error_type,
        )

    def _log(
        self,
        message: AgentMessage,
        event: ActionLogEvent,
        status: ActionLogStatus,
        *,
        phase: str,
        outcome: str,
        error_type: str | None = None,
    ) -> None:
        if self._logging_service is None:
            return

        payload = message.payload
        dispatch_id = payload.get(
            "dispatch_id",
            message.correlation_id,
        )

        metadata = {
            "phase": phase,
            "outcome": outcome,
            "dispatch_id": dispatch_id,
            "task_id": payload.get("task_id"),
            "goal_id": payload.get("goal_id"),
            "workflow_id": payload.get("workflow_id"),
            "workflow_step_id": payload.get(
                "workflow_step_id",
                payload.get("step_id"),
            ),
            "operation_id": payload.get("operation_id"),
            "sender_agent_id": message.sender_agent_id,
            "recipient_agent_id": message.recipient_agent_id,
            "owner_node_id": self._owner_node_id,
            "error_type": error_type,
        }

        try:
            self._logging_service.log(
                action=Action(
                    name="remote_task_execution",
                    category="distributed_execution",
                    target=str(dispatch_id),
                ),
                event=event,
                status=status,
                metadata=metadata,
            )
        except Exception:
            # Logging must not alter execution or idempotency behavior.
            pass

    @staticmethod
    def _require_string(value: object, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if not value.strip():
            raise ValueError(f"{field_name} must not be empty")