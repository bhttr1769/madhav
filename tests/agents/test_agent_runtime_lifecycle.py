import pytest

from brain.agents.agent_runtime_lifecycle import (
    AgentRuntimeLifecycle,
    AgentRuntimeLifecycleState,
    InvalidAgentRuntimeTransitionError,
)
from brain.agents.models.agent_runtime_state import AgentRuntimeState


def create_runtime_state(state):
    return AgentRuntimeState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        state=state.value,
    )


def test_created_can_transition_to_ready():
    current = create_runtime_state(AgentRuntimeLifecycleState.CREATED)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.READY,
    )

    assert result.state == AgentRuntimeLifecycleState.READY.value
    assert result.runtime_id == "runtime-1"
    assert result.agent_id == "agent-1"


def test_created_can_transition_to_failed():
    current = create_runtime_state(AgentRuntimeLifecycleState.CREATED)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.FAILED,
    )

    assert result.state == AgentRuntimeLifecycleState.FAILED.value


def test_ready_can_transition_to_running():
    current = create_runtime_state(AgentRuntimeLifecycleState.READY)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.RUNNING,
    )

    assert result.state == AgentRuntimeLifecycleState.RUNNING.value


def test_ready_can_transition_to_failed():
    current = create_runtime_state(AgentRuntimeLifecycleState.READY)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.FAILED,
    )

    assert result.state == AgentRuntimeLifecycleState.FAILED.value


def test_running_can_transition_to_paused():
    current = create_runtime_state(AgentRuntimeLifecycleState.RUNNING)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.PAUSED,
    )

    assert result.state == AgentRuntimeLifecycleState.PAUSED.value


def test_running_can_transition_to_stopped():
    current = create_runtime_state(AgentRuntimeLifecycleState.RUNNING)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.STOPPED,
    )

    assert result.state == AgentRuntimeLifecycleState.STOPPED.value


def test_running_can_transition_to_failed():
    current = create_runtime_state(AgentRuntimeLifecycleState.RUNNING)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.FAILED,
    )

    assert result.state == AgentRuntimeLifecycleState.FAILED.value


def test_paused_can_transition_to_running():
    current = create_runtime_state(AgentRuntimeLifecycleState.PAUSED)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.RUNNING,
    )

    assert result.state == AgentRuntimeLifecycleState.RUNNING.value


def test_paused_can_transition_to_stopped():
    current = create_runtime_state(AgentRuntimeLifecycleState.PAUSED)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.STOPPED,
    )

    assert result.state == AgentRuntimeLifecycleState.STOPPED.value


@pytest.mark.parametrize(
    "current_state,target_state",
    [
        (
            AgentRuntimeLifecycleState.CREATED,
            AgentRuntimeLifecycleState.RUNNING,
        ),
        (
            AgentRuntimeLifecycleState.CREATED,
            AgentRuntimeLifecycleState.STOPPED,
        ),
        (
            AgentRuntimeLifecycleState.READY,
            AgentRuntimeLifecycleState.CREATED,
        ),
        (
            AgentRuntimeLifecycleState.RUNNING,
            AgentRuntimeLifecycleState.CREATED,
        ),
        (
            AgentRuntimeLifecycleState.PAUSED,
            AgentRuntimeLifecycleState.CREATED,
        ),
        (
            AgentRuntimeLifecycleState.STOPPED,
            AgentRuntimeLifecycleState.RUNNING,
        ),
        (
            AgentRuntimeLifecycleState.FAILED,
            AgentRuntimeLifecycleState.READY,
        ),
    ],
)
def test_invalid_transition_is_rejected(current_state, target_state):
    current = create_runtime_state(current_state)

    with pytest.raises(InvalidAgentRuntimeTransitionError):
        AgentRuntimeLifecycle.transition(current, target_state)


def test_transition_does_not_mutate_original_state():
    current = create_runtime_state(AgentRuntimeLifecycleState.CREATED)

    result = AgentRuntimeLifecycle.transition(
        current,
        AgentRuntimeLifecycleState.READY,
    )

    assert current.state == AgentRuntimeLifecycleState.CREATED.value
    assert result.state == AgentRuntimeLifecycleState.READY.value
    assert current is not result


def test_can_transition_returns_true_for_valid_transition():
    assert AgentRuntimeLifecycle.can_transition(
        AgentRuntimeLifecycleState.CREATED.value,
        AgentRuntimeLifecycleState.READY,
    )


def test_can_transition_returns_false_for_invalid_transition():
    assert not AgentRuntimeLifecycle.can_transition(
        AgentRuntimeLifecycleState.CREATED.value,
        AgentRuntimeLifecycleState.RUNNING,
    )


def test_can_transition_returns_false_for_unknown_current_state():
    assert not AgentRuntimeLifecycle.can_transition(
        "UNKNOWN",
        AgentRuntimeLifecycleState.READY,
    )


def test_invalid_runtime_state_type_is_rejected():
    with pytest.raises(TypeError):
        AgentRuntimeLifecycle.transition(
            "invalid",
            AgentRuntimeLifecycleState.READY,
        )


def test_invalid_target_state_type_is_rejected():
    current = create_runtime_state(AgentRuntimeLifecycleState.CREATED)

    with pytest.raises(TypeError):
        AgentRuntimeLifecycle.transition(
            current,
            "READY",
        )