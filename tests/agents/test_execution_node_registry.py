
import pytest

from brain.agents.execution_node_registry import ExecutionNodeRegistry
from brain.agents.models.execution_node_identity import ExecutionNodeIdentity
from brain.agents.models.execution_node_registration import (
    ExecutionNodeRegistration,
)


def make_registration(
    node_id: str = "node-1",
    endpoint: str = "http://localhost:9000",
) -> ExecutionNodeRegistration:
    return ExecutionNodeRegistration(
        identity=ExecutionNodeIdentity(node_id=node_id),
        endpoint=endpoint,
    )


def test_register_and_get_node() -> None:
    registration = make_registration()
    registry = ExecutionNodeRegistry()

    registry.register(registration)

    assert registry.has("node-1")
    assert registry.get("node-1") is registration
    assert registry.all() == (registration,)


def test_constructor_registers_initial_nodes() -> None:
    registration = make_registration()
    registry = ExecutionNodeRegistry((registration,))

    assert registry.get("node-1") is registration


def test_duplicate_node_registration_is_rejected() -> None:
    registry = ExecutionNodeRegistry((make_registration(),))

    with pytest.raises(ValueError, match="already registered"):
        registry.register(
            make_registration(endpoint="http://localhost:9001")
        )


@pytest.mark.parametrize("node_id", ["", "   "])
def test_identity_rejects_empty_node_id(node_id: str) -> None:
    with pytest.raises(ValueError, match="node_id must not be empty"):
        ExecutionNodeIdentity(node_id=node_id)


def test_identity_rejects_non_string_node_id() -> None:
    with pytest.raises(TypeError, match="node_id must be a string"):
        ExecutionNodeIdentity(node_id=123)  # type: ignore[arg-type]


def test_registration_rejects_invalid_identity() -> None:
    with pytest.raises(
        TypeError,
        match="identity must be an ExecutionNodeIdentity",
    ):
        ExecutionNodeRegistration(
            identity="node-1",  # type: ignore[arg-type]
            endpoint="http://localhost:9000",
        )


@pytest.mark.parametrize("endpoint", ["", "   "])
def test_registration_rejects_empty_endpoint(endpoint: str) -> None:
    with pytest.raises(ValueError, match="endpoint must not be empty"):
        make_registration(endpoint=endpoint)


def test_registration_rejects_non_string_endpoint() -> None:
    with pytest.raises(TypeError, match="endpoint must be a string"):
        ExecutionNodeRegistration(
            identity=ExecutionNodeIdentity(node_id="node-1"),
            endpoint=123,  # type: ignore[arg-type]
        )


def test_get_unknown_node_raises_clear_error() -> None:
    registry = ExecutionNodeRegistry()

    with pytest.raises(KeyError, match="execution node not found: missing"):
        registry.get("missing")


def test_unregister_removes_node() -> None:
    registry = ExecutionNodeRegistry((make_registration(),))

    registry.unregister("node-1")

    assert not registry.has("node-1")
    assert registry.all() == ()


def test_unregister_unknown_node_raises_clear_error() -> None:
    registry = ExecutionNodeRegistry()

    with pytest.raises(KeyError, match="execution node not found: missing"):
        registry.unregister("missing")


@pytest.mark.parametrize("node_id", ["", "   "])
def test_registry_rejects_empty_lookup_id(node_id: str) -> None:
    registry = ExecutionNodeRegistry()

    with pytest.raises(ValueError, match="node_id must not be empty"):
        registry.has(node_id)


def test_registry_rejects_non_string_lookup_id() -> None:
    registry = ExecutionNodeRegistry()

    with pytest.raises(TypeError, match="node_id must be a string"):
        registry.has(123)  # type: ignore[arg-type]
