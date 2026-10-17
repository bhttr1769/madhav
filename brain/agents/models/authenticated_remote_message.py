
from dataclasses import dataclass
import json

from brain.agents.models.agent_message import AgentMessage, AgentMessageType


@dataclass(frozen=True)
class AuthenticatedRemoteMessage:
    sender_node_id: str
    recipient_node_id: str
    issued_at: int
    nonce: str
    message: AgentMessage
    signature: str

    def __post_init__(self) -> None:
        for field_name in ("sender_node_id", "recipient_node_id", "nonce"):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if type(self.issued_at) is not int:
            raise TypeError("issued_at must be an integer")

        if not isinstance(self.message, AgentMessage):
            raise TypeError("message must be an AgentMessage")

        if not isinstance(self.signature, str):
            raise TypeError("signature must be a string")

        if not self.signature.strip():
            raise ValueError("signature must not be empty")

    def unsigned_dict(self) -> dict[str, object]:
        return {
            "sender_node_id": self.sender_node_id,
            "recipient_node_id": self.recipient_node_id,
            "issued_at": self.issued_at,
            "nonce": self.nonce,
            "message": {
                "id": self.message.id,
                "sender_agent_id": self.message.sender_agent_id,
                "recipient_agent_id": self.message.recipient_agent_id,
                "message_type": self.message.message_type.value,
                "payload": self.message.payload,
                "correlation_id": self.message.correlation_id,
            },
        }

    def to_wire_bytes(self) -> bytes:
        data = self.unsigned_dict()
        data["signature"] = self.signature
        return json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")

    @classmethod
    def from_wire_bytes(
        cls,
        wire_bytes: bytes,
    ) -> "AuthenticatedRemoteMessage":
        if not isinstance(wire_bytes, bytes):
            raise TypeError("wire_bytes must be bytes")

        try:
            data = json.loads(wire_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid remote message encoding") from exc

        if not isinstance(data, dict):
            raise ValueError("remote message envelope must be an object")

        expected_keys = {
            "sender_node_id",
            "recipient_node_id",
            "issued_at",
            "nonce",
            "message",
            "signature",
        }
        if set(data) != expected_keys:
            raise ValueError("remote message envelope has invalid fields")

        message_data = data["message"]
        if not isinstance(message_data, dict):
            raise ValueError("message must be an object")

        expected_message_keys = {
            "id",
            "sender_agent_id",
            "recipient_agent_id",
            "message_type",
            "payload",
            "correlation_id",
        }
        if set(message_data) != expected_message_keys:
            raise ValueError("remote agent message has invalid fields")

        if not isinstance(message_data["payload"], dict):
            raise ValueError("message payload must be an object")

        try:
            message_type = AgentMessageType(message_data["message_type"])
            message = AgentMessage(
                id=message_data["id"],
                sender_agent_id=message_data["sender_agent_id"],
                recipient_agent_id=message_data["recipient_agent_id"],
                message_type=message_type,
                payload=message_data["payload"],
                correlation_id=message_data["correlation_id"],
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid agent message in envelope") from exc

        try:
            return cls(
                sender_node_id=data["sender_node_id"],
                recipient_node_id=data["recipient_node_id"],
                issued_at=data["issued_at"],
                nonce=data["nonce"],
                message=message,
                signature=data["signature"],
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid remote message envelope") from exc
