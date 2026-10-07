import pytest

from brain.agents.models.agent_runtime_state import AgentRuntimeState


def test_agent_runtime_state_stores_identity_and_state():
    state = AgentRuntimeState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        state="INITIALIZED",
    )

    assert state.runtime_id == "runtime-1"
    assert state.agent_id == "agent-1"
    assert state.state == "INITIALIZED"


def test_agent_runtime_state_is_immutable():
    state = AgentRuntimeState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        state="INITIALIZED",
    )

    with pytest.raises(Exception):
        state.state = "RUNNING"


@pytest.mark.parametrize("runtime_id", ["", "   "])
def test_empty_runtime_id_is_rejected(runtime_id):
    with pytest.raises(ValueError):
        AgentRuntimeState(
            runtime_id=runtime_id,
            agent_id="agent-1",
            state="INITIALIZED",
        )


def test_non_string_runtime_id_is_rejected():
    with pytest.raises(TypeError):
        AgentRuntimeState(
            runtime_id=123,
            agent_id="agent-1",
            state="INITIALIZED",
        )


@pytest.mark.parametrize("agent_id", ["", "   "])
def test_empty_agent_id_is_rejected(agent_id):
    with pytest.raises(ValueError):
        AgentRuntimeState(
            runtime_id="runtime-1",
            agent_id=agent_id,
            state="INITIALIZED",
        )


def test_non_string_agent_id_is_rejected():
    with pytest.raises(TypeError):
        AgentRuntimeState(
            runtime_id="runtime-1",
            agent_id=123,
            state="INITIALIZED",
        )


@pytest.mark.parametrize("state", ["", "   "])
def test_empty_state_is_rejected(state):
    with pytest.raises(ValueError):
        AgentRuntimeState(
            runtime_id="runtime-1",
            agent_id="agent-1",
            state=state,
        )


def test_non_string_state_is_rejected():
    with pytest.raises(TypeError):
        AgentRuntimeState(
            runtime_id="runtime-1",
            agent_id="agent-1",
            state=123,
        )


def test_runtime_states_are_independent():
    state_one = AgentRuntimeState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        state="INITIALIZED",
    )

    state_two = AgentRuntimeState(
        runtime_id="runtime-2",
        agent_id="agent-1",
        state="INITIALIZED",
    )

    assert state_one.runtime_id != state_two.runtime_id


def test_equal_runtime_states_are_equal():
    state_one = AgentRuntimeState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        state="INITIALIZED",
    )

    state_two = AgentRuntimeState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        state="INITIALIZED",
    )

    assert state_one == state_two