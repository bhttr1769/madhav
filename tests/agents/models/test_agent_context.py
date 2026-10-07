import pytest

from brain.agents.models.agent_context import AgentContext


def test_agent_context_can_be_created():
    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    assert context.runtime_id == "runtime-1"
    assert context.agent_id == "agent-1"


def test_context_sources_default_to_none():
    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    assert context.user is None
    assert context.project is None
    assert context.environment is None
    assert context.memory is None
    assert context.knowledge is None
    assert context.perception is None
    assert context.runtime is None


def test_context_can_hold_existing_source_objects():
    project = object()
    environment = object()
    memory = object()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=project,
        environment=environment,
        memory=memory,
    )

    assert context.project is project
    assert context.environment is environment
    assert context.memory is memory


def test_agent_context_is_immutable():
    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    with pytest.raises(AttributeError):
        context.runtime_id = "runtime-2"


def test_runtime_id_must_be_string():
    with pytest.raises(TypeError):
        AgentContext(
            runtime_id=123,
            agent_id="agent-1",
        )


def test_runtime_id_must_not_be_empty():
    with pytest.raises(ValueError):
        AgentContext(
            runtime_id="",
            agent_id="agent-1",
        )


def test_agent_id_must_be_string():
    with pytest.raises(TypeError):
        AgentContext(
            runtime_id="runtime-1",
            agent_id=123,
        )


def test_agent_id_must_not_be_empty():
    with pytest.raises(ValueError):
        AgentContext(
            runtime_id="runtime-1",
            agent_id="",
        )