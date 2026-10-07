from brain.agents.agent_context_builder import AgentContextBuilder
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.context_source import ContextSource
from brain.agents.context_source_coordinator import ContextSourceCoordinator
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.agent_context import AgentContext
from brain.agents.models.context_integration_result import (
    ContextIntegrationResult,
)


class AgentContextIntegrator:
    """
    Integrates coordinated source results into an AgentContext.

    AgentRuntime is the authoritative source for runtime identity.
    This class coordinates existing components only.
    It does not retrieve, transform, or persist source data.
    """

    def __init__(
        self,
        coordinator: ContextSourceCoordinator,
        builder: AgentContextBuilder,
    ) -> None:
        self._coordinator = coordinator
        self._builder = builder

    def integrate(
        self,
        runtime: AgentRuntime,
        providers: tuple,
        requested_sources: frozenset[ContextSource],
    ) -> ContextIntegrationResult:

        if not isinstance(runtime, AgentRuntime):
            raise TypeError("runtime must be an AgentRuntime")

        source_results = self._coordinator.coordinate(
            providers=providers,
            requested_sources=requested_sources,
        )

        values = {}

        for source in ContextSource:
            result = source_results[source]

            if result.status == ContextSourceStatus.AVAILABLE:
                values[source.value] = result.value

        context = self._builder.build(
            runtime_id=runtime.runtime_id,
            agent_id=runtime.agent_id,
            user=values.get("user"),
            project=values.get("project"),
            environment=values.get("environment"),
            memory=values.get("memory"),
            knowledge=values.get("knowledge"),
            perception=values.get("perception"),
            runtime=runtime,
        )

        return ContextIntegrationResult(
            context=context,
            source_results=source_results,
        )