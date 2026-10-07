from brain.agents.agent_context_integrator import AgentContextIntegrator
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.context_persistence import ContextPersistence
from brain.agents.models.context_integration_result import (
    ContextIntegrationResult,
)


class AgentContextRestorer:
    """
    Restores agent context using persisted restoration metadata
    and existing context providers.
    """

    def __init__(
        self,
        persistence: ContextPersistence,
        integrator: AgentContextIntegrator,
    ) -> None:
        self._persistence = persistence
        self._integrator = integrator

    def restore(
        self,
        runtime: AgentRuntime,
        providers: tuple,
    ) -> ContextIntegrationResult:

        if not isinstance(runtime, AgentRuntime):
            raise TypeError("runtime must be an AgentRuntime")

        state = self._persistence.load(runtime.runtime_id)

        if state.runtime_id != runtime.runtime_id:
            raise ValueError(
                "persisted runtime_id does not match runtime"
            )

        if state.agent_id != runtime.agent_id:
            raise ValueError(
                "persisted agent_id does not match runtime"
            )

        return self._integrator.integrate(
            runtime=runtime,
            providers=providers,
            requested_sources=state.requested_sources,
        )