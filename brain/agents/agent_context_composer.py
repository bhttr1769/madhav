from brain.agents.agent_runtime import AgentRuntime
from brain.agents.models.agent_context import AgentContext


class AgentContextComposer:
    """
    Composes a base agent context with a partial context update.

    The composer only merges existing context references.
    It does not retrieve, transform, persist, or interpret source data.
    """

    def compose(
        self,
        base: AgentContext,
        update: AgentContext,
    ) -> AgentContext:

        if not isinstance(base, AgentContext):
            raise TypeError("base must be an AgentContext")

        if not isinstance(update, AgentContext):
            raise TypeError("update must be an AgentContext")

        if base.runtime_id != update.runtime_id:
            raise ValueError(
                "base and update must have the same runtime_id"
            )

        if base.agent_id != update.agent_id:
            raise ValueError(
                "base and update must have the same agent_id"
            )

        if (
            base.runtime is not None
            and not isinstance(base.runtime, AgentRuntime)
        ):
            raise ValueError(
                "base runtime must be an AgentRuntime"
            )

        if (
            update.runtime is not None
            and not isinstance(update.runtime, AgentRuntime)
        ):
            raise ValueError(
                "update runtime must be an AgentRuntime"
            )

        if (
            base.runtime is not None
            and base.runtime.runtime_id != base.runtime_id
        ):
            raise ValueError(
                "base runtime.runtime_id must match base runtime_id"
            )

        if (
            update.runtime is not None
            and update.runtime.runtime_id != update.runtime_id
        ):
            raise ValueError(
                "update runtime.runtime_id must match update runtime_id"
            )

        if (
            base.runtime is not None
            and base.runtime.agent_id != base.agent_id
        ):
            raise ValueError(
                "base runtime.agent_id must match base agent_id"
            )

        if (
            update.runtime is not None
            and update.runtime.agent_id != update.agent_id
        ):
            raise ValueError(
                "update runtime.agent_id must match update agent_id"
            )

        if (
            base.runtime is not None
            and update.runtime is not None
            and base.runtime is not update.runtime
        ):
            raise ValueError(
                "base and update must reference the same AgentRuntime"
            )

        runtime = (
            update.runtime
            if update.runtime is not None
            else base.runtime
        )

        return AgentContext(
            runtime_id=base.runtime_id,
            agent_id=base.agent_id,
            user=(
                update.user
                if update.user is not None
                else base.user
            ),
            project=(
                update.project
                if update.project is not None
                else base.project
            ),
            environment=(
                update.environment
                if update.environment is not None
                else base.environment
            ),
            memory=(
                update.memory
                if update.memory is not None
                else base.memory
            ),
            knowledge=(
                update.knowledge
                if update.knowledge is not None
                else base.knowledge
            ),
            perception=(
                update.perception
                if update.perception is not None
                else base.perception
            ),
            runtime=runtime,
        )