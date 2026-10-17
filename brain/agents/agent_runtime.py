
from uuid import uuid4

from brain.agents.agent_runtime_lifecycle import (
    AgentRuntimeLifecycle,
    AgentRuntimeLifecycleState,
)
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_runtime_state import AgentRuntimeState
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.organization.authority_execution_context import (
    authority_execution_context,
)


class AgentRuntime:
    def __init__(
        self,
        agent_definition: AgentDefinition,
        capability_runtime: CapabilityRuntime,
        runtime_id: str | None = None,
        organization_id: str | None = None,
    ):
        if not isinstance(agent_definition, AgentDefinition):
            raise TypeError("agent_definition must be an AgentDefinition")

        if not isinstance(capability_runtime, CapabilityRuntime):
            raise TypeError("capability_runtime must be a CapabilityRuntime")

        if runtime_id is None:
            runtime_id = str(uuid4())

        if not isinstance(runtime_id, str):
            raise TypeError("runtime_id must be a string")

        if not runtime_id.strip():
            raise ValueError("runtime_id must not be empty")

        if organization_id is not None:
            if not isinstance(organization_id, str):
                raise TypeError("organization_id must be a string or None")

            if not organization_id.strip():
                raise ValueError("organization_id must not be empty")

        self._agent_definition = agent_definition
        self._capability_runtime = capability_runtime
        self._organization_id = organization_id

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
    def organization_id(self) -> str | None:
        return self._organization_id

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
        *,
        authority_agent_id: str | None = None,
    ) -> CapabilityExecutionResult:
        if not isinstance(capability_id, str):
            raise TypeError("capability_id must be a string")

        if not capability_id.strip():
            raise ValueError("capability_id must not be empty")

        if self._state.state != AgentRuntimeLifecycleState.RUNNING.value:
            raise RuntimeError(
                "agent runtime must be RUNNING to execute a capability"
            )

        if capability_id not in self._agent_definition.capabilities:
            raise ValueError(
                f"capability '{capability_id}' is not associated "
                f"with agent '{self.agent_id}'"
            )

        if authority_agent_id is None:
            execution_agent_id = self.agent_id
        else:
            if not isinstance(authority_agent_id, str):
                raise TypeError("authority_agent_id must be a string")

            if not authority_agent_id.strip():
                raise ValueError("authority_agent_id must not be empty")

            execution_agent_id = authority_agent_id

        request = CapabilityExecutionRequest(
            capability_id=capability_id,
            input_data=input_data,
        )

        # RemoteTaskExecutionReceiver must authorize the requesting agent
        # before passing authority_agent_id. This context makes that identity
        # visible to existing capability-level SafetyService checks.
        with authority_execution_context(
            agent_id=execution_agent_id,
            organization_id=self._organization_id,
        ):
            return self._capability_runtime.execute(request)

    def can_operate_on_goal(self, goal: Goal) -> bool:
        if not isinstance(goal, Goal):
            raise TypeError("goal must be a Goal")

        return goal.agent_id == self.agent_id

    def authorize_goal(self, goal: Goal) -> None:
        if not self.can_operate_on_goal(goal):
            raise ValueError(
                "goal does not belong to the runtime's agent"
            )

    def can_operate_on_task(
        self,
        task: AgentTask,
        goal: Goal,
    ) -> bool:
        if not isinstance(task, AgentTask):
            raise TypeError("task must be an AgentTask")

        if not isinstance(goal, Goal):
            raise TypeError("goal must be a Goal")

        return (
            task.goal_id == goal.id
            and goal.agent_id == self.agent_id
        )

    def authorize_task(
        self,
        task: AgentTask,
        goal: Goal,
    ) -> None:
        if not self.can_operate_on_task(task, goal):
            raise ValueError(
                "task does not belong to the runtime's agent "
                "through the supplied goal"
            )
