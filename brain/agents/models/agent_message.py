from dataclasses import dataclass
from enum import Enum


class AgentMessageType(Enum):
    """
    Defines the semantic type of an agent-to-agent message.
    """

    INFORMATION = "information"
    REQUEST = "request"
    RESPONSE = "response"
    HANDOFF = "handoff"


@dataclass(frozen=True)
class AgentMessage:
    """
    Represents a message sent from one agent to another.

    The message contains addressing, semantic type, an opaque
    payload, and an optional correlation reference.

    It does not perform delivery, execution, authorization,
    persistence, or payload interpretation.
    """

    id: str
    sender_agent_id: str
    recipient_agent_id: str
    message_type: AgentMessageType
    payload: dict[str, object]
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")

        if not self.id.strip():
            raise ValueError("id must be a non-empty string")

        if not isinstance(self.sender_agent_id, str):
            raise TypeError("sender_agent_id must be a string")

        if not self.sender_agent_id.strip():
            raise ValueError(
                "sender_agent_id must be a non-empty string"
            )

        if not isinstance(self.recipient_agent_id, str):
            raise TypeError("recipient_agent_id must be a string")

        if not self.recipient_agent_id.strip():
            raise ValueError(
                "recipient_agent_id must be a non-empty string"
            )

        if not isinstance(self.message_type, AgentMessageType):
            raise TypeError(
                "message_type must be an AgentMessageType"
            )

        if not isinstance(self.payload, dict):
            raise TypeError("payload must be a dict")

        if self.correlation_id is not None:
            if not isinstance(self.correlation_id, str):
                raise TypeError(
                    "correlation_id must be a string or None"
                )

            if not self.correlation_id.strip():
                raise ValueError(
                    "correlation_id must be a non-empty string "
                    "when provided"
                )