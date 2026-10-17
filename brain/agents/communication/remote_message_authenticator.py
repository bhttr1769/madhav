
import hashlib
import hmac
import json
import secrets
import time
from collections.abc import Mapping
from threading import Lock
from typing import Callable

from brain.agents.models.agent_message import AgentMessage
from brain.agents.models.authenticated_remote_message import (
    AuthenticatedRemoteMessage,
)


class RemoteMessageAuthenticator:
    """Signs and verifies remote messages using per-peer shared secrets."""

    def __init__(
        self,
        local_node_id: str,
        peer_secrets: Mapping[str, bytes],
        max_clock_skew_seconds: int = 300,
        clock: Callable[[], float] = time.time,
        nonce_factory: Callable[[], str] = (
            lambda: secrets.token_urlsafe(24)
        ),
    ) -> None:
        self._validate_non_empty_string(local_node_id, "local_node_id")

        if not isinstance(peer_secrets, Mapping):
            raise TypeError("peer_secrets must be a mapping")

        if type(max_clock_skew_seconds) is not int:
            raise TypeError("max_clock_skew_seconds must be an integer")
        if max_clock_skew_seconds <= 0:
            raise ValueError("max_clock_skew_seconds must be positive")

        if not callable(clock):
            raise TypeError("clock must be callable")
        if not callable(nonce_factory):
            raise TypeError("nonce_factory must be callable")

        validated_secrets: dict[str, bytes] = {}
        for node_id, secret in peer_secrets.items():
            self._validate_non_empty_string(node_id, "peer node ID")

            if not isinstance(secret, bytes):
                raise TypeError("peer secrets must be bytes")
            if len(secret) < 32:
                raise ValueError(
                    "each peer secret must contain at least 32 bytes"
                )

            validated_secrets[node_id] = secret

        self._local_node_id = local_node_id
        self._peer_secrets = validated_secrets
        self._max_clock_skew_seconds = max_clock_skew_seconds
        self._clock = clock
        self._nonce_factory = nonce_factory
        self._seen_nonces: dict[tuple[str, str], int] = {}
        self._nonce_lock = Lock()

    def seal(
        self,
        message: AgentMessage,
        recipient_node_id: str,
    ) -> bytes:
        if not isinstance(message, AgentMessage):
            raise TypeError("message must be an AgentMessage")

        self._validate_non_empty_string(
            recipient_node_id, "recipient_node_id"
        )

        if recipient_node_id == self._local_node_id:
            raise ValueError("recipient node must be remote")

        secret = self._peer_secrets.get(recipient_node_id)
        if secret is None:
            raise ValueError(
                f"no shared secret configured for node: {recipient_node_id}"
            )

        nonce = self._nonce_factory()
        self._validate_non_empty_string(nonce, "nonce")

        unsigned = AuthenticatedRemoteMessage(
            sender_node_id=self._local_node_id,
            recipient_node_id=recipient_node_id,
            issued_at=int(self._clock()),
            nonce=nonce,
            message=message,
            signature="pending",
        )

        signature = hmac.new(
            secret,
            self._canonical_bytes(unsigned.unsigned_dict()),
            hashlib.sha256,
        ).hexdigest()

        envelope = AuthenticatedRemoteMessage(
            sender_node_id=unsigned.sender_node_id,
            recipient_node_id=unsigned.recipient_node_id,
            issued_at=unsigned.issued_at,
            nonce=unsigned.nonce,
            message=unsigned.message,
            signature=signature,
        )

        return envelope.to_wire_bytes()

    def open(self, wire_bytes: bytes) -> AgentMessage:
        envelope = AuthenticatedRemoteMessage.from_wire_bytes(wire_bytes)

        if envelope.recipient_node_id != self._local_node_id:
            raise ValueError("message is addressed to a different node")

        now = int(self._clock())
        if abs(now - envelope.issued_at) > self._max_clock_skew_seconds:
            raise ValueError("remote message has expired or is not yet valid")

        secret = self._peer_secrets.get(envelope.sender_node_id)
        if secret is None:
            raise ValueError(
                f"unknown sending node: {envelope.sender_node_id}"
            )

        expected_signature = hmac.new(
            secret,
            self._canonical_bytes(envelope.unsigned_dict()),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            expected_signature,
            envelope.signature,
        ):
            raise ValueError("remote message authentication failed")

        self._record_nonce(envelope.sender_node_id, envelope.nonce, now)
        return envelope.message

    def _record_nonce(
        self,
        sender_node_id: str,
        nonce: str,
        now: int,
    ) -> None:
        replay_key = (sender_node_id, nonce)
        oldest_valid_timestamp = now - self._max_clock_skew_seconds

        with self._nonce_lock:
            expired_keys = [
                key
                for key, timestamp in self._seen_nonces.items()
                if timestamp < oldest_valid_timestamp
            ]
            for key in expired_keys:
                del self._seen_nonces[key]

            if replay_key in self._seen_nonces:
                raise ValueError("replayed remote message rejected")

            self._seen_nonces[replay_key] = now

    @staticmethod
    def _canonical_bytes(data: dict[str, object]) -> bytes:
        try:
            encoded = json.dumps(
                data,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "remote message payload must contain JSON-compatible values"
            ) from exc

        return encoded.encode("utf-8")

    @staticmethod
    def _validate_non_empty_string(value: str, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if not value.strip():
            raise ValueError(f"{field_name} must not be empty")
