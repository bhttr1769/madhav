from enum import Enum

from brain.agents.models.agent_runtime_state import AgentRuntimeState


class AgentRuntimeLifecycleState(str, Enum):
    CREATED = "CREATED"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class InvalidAgentRuntimeTransitionError(ValueError):
    """Raised when an agent runtime attempts an invalid lifecycle transition."""


class AgentRuntimeLifecycle:
    _TRANSITIONS = {
        AgentRuntimeLifecycleState.CREATED: {
            AgentRuntimeLifecycleState.READY,
            AgentRuntimeLifecycleState.FAILED,
        },
        AgentRuntimeLifecycleState.READY: {
            AgentRuntimeLifecycleState.RUNNING,
            AgentRuntimeLifecycleState.FAILED,
        },
        AgentRuntimeLifecycleState.RUNNING: {
            AgentRuntimeLifecycleState.PAUSED,
            AgentRuntimeLifecycleState.STOPPED,
            AgentRuntimeLifecycleState.FAILED,
        },
        AgentRuntimeLifecycleState.PAUSED: {
            AgentRuntimeLifecycleState.RUNNING,
            AgentRuntimeLifecycleState.STOPPED,
        },
        AgentRuntimeLifecycleState.STOPPED: set(),
        AgentRuntimeLifecycleState.FAILED: set(),
    }

    @classmethod
    def transition(
        cls,
        runtime_state: AgentRuntimeState,
        target_state: AgentRuntimeLifecycleState,
    ) -> AgentRuntimeState:
        if not isinstance(runtime_state, AgentRuntimeState):
            raise TypeError("runtime_state must be an AgentRuntimeState")

        if not isinstance(target_state, AgentRuntimeLifecycleState):
            raise TypeError(
                "target_state must be an AgentRuntimeLifecycleState"
            )

        current_state = runtime_state.state

        try:
            current_lifecycle_state = AgentRuntimeLifecycleState(current_state)
        except ValueError as exc:
            raise InvalidAgentRuntimeTransitionError(
                f"Unknown current lifecycle state: {current_state}"
            ) from exc

        allowed_states = cls._TRANSITIONS[current_lifecycle_state]

        if target_state not in allowed_states:
            raise InvalidAgentRuntimeTransitionError(
                f"Invalid agent runtime transition: "
                f"{current_lifecycle_state.value} -> {target_state.value}"
            )

        return AgentRuntimeState(
            runtime_id=runtime_state.runtime_id,
            agent_id=runtime_state.agent_id,
            state=target_state.value,
        )

    @classmethod
    def can_transition(
        cls,
        current_state: str,
        target_state: AgentRuntimeLifecycleState,
    ) -> bool:
        if not isinstance(current_state, str):
            raise TypeError("current_state must be a string")

        if not isinstance(target_state, AgentRuntimeLifecycleState):
            raise TypeError(
                "target_state must be an AgentRuntimeLifecycleState"
            )

        try:
            current_lifecycle_state = AgentRuntimeLifecycleState(current_state)
        except ValueError:
            return False

        return target_state in cls._TRANSITIONS[current_lifecycle_state]