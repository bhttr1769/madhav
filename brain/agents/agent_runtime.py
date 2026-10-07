from uuid import uuid4

from brain.agents.agent_runtime_lifecycle import (
    AgentRuntimeLifecycle,
    AgentRuntimeLifecycleState,
)
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_runtime_state import AgentRuntimeState
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


class AgentRuntime:
    def __init__(
        self,
        agent_definition: AgentDefinition,
        capability_runtime: CapabilityRuntime,
        runtime_id: str | None = None,
    ):
        if not isinstance(agent_definition, AgentDefinition):
            raise TypeError(
                "agent_definition must be an AgentDefinition"
            )

        if not isinstance(capability_runtime, CapabilityRuntime):
            raise TypeError(
                "capability_runtime must be a CapabilityRuntime"
            )

        if runtime_id is None:
            runtime_id = str(uuid4())

        if not isinstance(runtime_id, str):
            raise TypeError("runtime_id must be a string")

        if not runtime_id.strip():
            raise ValueError("runtime_id must not be empty")

        self._agent_definition = agent_definition
        self._capability_runtime = capability_runtime

        self._state = AgentRuntimeState(
            runtime_id=runtime_id,
            agent_id=agent_definition.identity.id,
            state=AgentRuntimeLifecycleState.CREATED.value,
        )

    @property
    def agent_definition(self) -> AgentDefinition:
        return self._agent_definition

    @property
    def runtime_id(self) -> str:
        return self._state.runtime_id

    @property
    def agent_id(self) -> str:
        return self._state.agent_id

    @property
    def state(self) -> AgentRuntimeState:
        return self._state

    def transition_to(
        self,
        target_state: AgentRuntimeLifecycleState,
    ) -> AgentRuntimeState:
        self._state = AgentRuntimeLifecycle.transition(
            self._state,
            target_state,
        )

        return self._state

    def execute_capability(
        self,
        capability_id: str,
        input_data: object,
    ) -> CapabilityExecutionResult:
        if not isinstance(capability_id, str):
            raise TypeError(
                "capability_id must be a string"
            )

        if not capability_id.strip():
            raise ValueError(
                "capability_id must not be empty"
            )

        if self._state.state != AgentRuntimeLifecycleState.RUNNING.value:
            raise RuntimeError(
                "agent runtime must be RUNNING to execute a capability"
            )

        if capability_id not in self._agent_definition.capabilities:
            raise ValueError(
                f"capability '{capability_id}' is not associated "
                f"with agent '{self.agent_id}'"
            )

        request = CapabilityExecutionRequest(
            capability_id=capability_id,
            input_data=input_data,
        )

        return self._capability_runtime.execute(request)