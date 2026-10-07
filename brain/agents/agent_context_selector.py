from brain.agents.context_source import ContextSource
from brain.agents.models.agent_context import AgentContext


class AgentContextSelector:
    """
    Selects existing context sources from an AgentContext.

    This class does not retrieve, rank, transform, or generate context.
    """

    def select(
        self,
        context: AgentContext,
        sources: frozenset[ContextSource],
    ) -> AgentContext:
        if not isinstance(context, AgentContext):
            raise TypeError("context must be an AgentContext")

        if not isinstance(sources, frozenset):
            raise TypeError("sources must be a frozenset")

        for source in sources:
            if not isinstance(source, ContextSource):
                raise TypeError(
                    "sources must contain only ContextSource values"
                )

        return AgentContext(
            runtime_id=context.runtime_id,
            agent_id=context.agent_id,
            user=(
                context.user
                if ContextSource.USER in sources
                else None
            ),
            project=(
                context.project
                if ContextSource.PROJECT in sources
                else None
            ),
            environment=(
                context.environment
                if ContextSource.ENVIRONMENT in sources
                else None
            ),
            memory=(
                context.memory
                if ContextSource.MEMORY in sources
                else None
            ),
            knowledge=(
                context.knowledge
                if ContextSource.KNOWLEDGE in sources
                else None
            ),
            perception=(
                context.perception
                if ContextSource.PERCEPTION in sources
                else None
            ),
            runtime=(
                context.runtime
                if ContextSource.RUNTIME in sources
                else None
            ),
        )