import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_registry import AgentRuntimeRegistry
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.capabilities.capability_runtime import CapabilityRuntime


class FakeCapabilityRuntime(CapabilityRuntime):
    def __init__(self):
        pass

    def execute(self, request):
        raise NotImplementedError


def create_agent_definition(
    agent_id="agent-1",
    name="Test Agent",
):
    return AgentDefinition(
        identity=AgentIdentity(
            id=agent_id,
            name=name,
        ),
        description="Test agent definition",
        version="1.0.0",
        capabilities=frozenset(),
    )


def create_runtime(
    runtime_id="runtime-1",
    agent_id="agent-1",
):
    return AgentRuntime(
        create_agent_definition(agent_id=agent_id),
        FakeCapabilityRuntime(),
        runtime_id=runtime_id,
    )


def test_register_and_get_runtime():
    registry = AgentRuntimeRegistry()
    runtime = create_runtime()

    registry.register(runtime)

    assert registry.get("runtime-1") is runtime


def test_register_preserves_runtime_instance():
    registry = AgentRuntimeRegistry()
    runtime = create_runtime()

    registry.register(runtime)

    assert registry.get("runtime-1") is runtime


def test_has_returns_true_for_registered_runtime():
    registry = AgentRuntimeRegistry()
    runtime = create_runtime()

    registry.register(runtime)

    assert registry.has("runtime-1") is True


def test_has_returns_false_for_missing_runtime():
    registry = AgentRuntimeRegistry()

    assert registry.has("missing-runtime") is False


def test_all_returns_registered_runtimes():
    registry = AgentRuntimeRegistry()

    first = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    second = create_runtime(
        runtime_id="runtime-2",
        agent_id="agent-2",
    )

    registry.register(first)
    registry.register(second)

    assert registry.all() == (
        first,
        second,
    )


def test_unregister_removes_runtime():
    registry = AgentRuntimeRegistry()
    runtime = create_runtime()

    registry.register(runtime)
    registry.unregister("runtime-1")

    assert registry.has("runtime-1") is False
    assert registry.all() == ()


def test_duplicate_runtime_registration_is_rejected():
    registry = AgentRuntimeRegistry()

    first = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    second = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-2",
    )

    registry.register(first)

    with pytest.raises(ValueError):
        registry.register(second)


def test_register_invalid_type_is_rejected():
    registry = AgentRuntimeRegistry()

    with pytest.raises(TypeError):
        registry.register(object())


def test_get_missing_runtime_raises_key_error():
    registry = AgentRuntimeRegistry()

    with pytest.raises(KeyError):
        registry.get("missing-runtime")


def test_unregister_missing_runtime_raises_key_error():
    registry = AgentRuntimeRegistry()

    with pytest.raises(KeyError):
        registry.unregister("missing-runtime")


@pytest.mark.parametrize(
    "runtime_id",
    [
        "",
        "   ",
    ],
)
def test_get_rejects_empty_runtime_id(runtime_id):
    registry = AgentRuntimeRegistry()

    with pytest.raises(ValueError):
        registry.get(runtime_id)


@pytest.mark.parametrize(
    "runtime_id",
    [
        "",
        "   ",
    ],
)
def test_has_rejects_empty_runtime_id(runtime_id):
    registry = AgentRuntimeRegistry()

    with pytest.raises(ValueError):
        registry.has(runtime_id)


@pytest.mark.parametrize(
    "runtime_id",
    [
        "",
        "   ",
    ],
)
def test_unregister_rejects_empty_runtime_id(runtime_id):
    registry = AgentRuntimeRegistry()

    with pytest.raises(ValueError):
        registry.unregister(runtime_id)


def test_get_rejects_non_string_runtime_id():
    registry = AgentRuntimeRegistry()

    with pytest.raises(TypeError):
        registry.get(123)


def test_has_rejects_non_string_runtime_id():
    registry = AgentRuntimeRegistry()

    with pytest.raises(TypeError):
        registry.has(123)


def test_unregister_rejects_non_string_runtime_id():
    registry = AgentRuntimeRegistry()

    with pytest.raises(TypeError):
        registry.unregister(123)


def test_multiple_runtimes_of_same_agent_are_supported():
    registry = AgentRuntimeRegistry()

    first = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    second = create_runtime(
        runtime_id="runtime-2",
        agent_id="agent-1",
    )

    registry.register(first)
    registry.register(second)

    assert registry.all() == (
        first,
        second,
    )