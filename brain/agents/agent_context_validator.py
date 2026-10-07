from brain.agents.context_source import ContextSource
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.agent_context import AgentContext
from brain.agents.models.context_integration_result import (
    ContextIntegrationResult,
)
from brain.agents.models.context_validation import ContextValidation
from brain.agents.agent_runtime import AgentRuntime


class AgentContextValidator:
    """
    Performs structural consistency validation for agent context.

    This validator does not perform semantic reasoning or source retrieval.
    """

    def validate(
        self,
        context: AgentContext,
    ) -> ContextValidation:

        if not isinstance(context, AgentContext):
            raise TypeError("context must be an AgentContext")

        errors: list[str] = []

        if not context.runtime_id.strip():
            errors.append("runtime_id must not be empty")

        if not context.agent_id.strip():
            errors.append("agent_id must not be empty")

        if context.runtime is not None:
            if not isinstance(context.runtime, AgentRuntime):
                errors.append(
                    "runtime must be an AgentRuntime"
                )
            else:
                if context.runtime.runtime_id != context.runtime_id:
                    errors.append(
                        "runtime.runtime_id must match context.runtime_id"
                    )

                if context.runtime.agent_id != context.agent_id:
                    errors.append(
                        "runtime.agent_id must match context.agent_id"
                    )

        return ContextValidation(
            valid=not errors,
            errors=tuple(errors),
        )

    def validate_integration(
        self,
        result: ContextIntegrationResult,
    ) -> ContextValidation:

        if not isinstance(result, ContextIntegrationResult):
            raise TypeError(
                "result must be a ContextIntegrationResult"
            )

        validation = self.validate(result.context)

        errors = list(validation.errors)

        for source in ContextSource:
            source_result = result.source_results.get(source)

            if source_result is None:
                errors.append(
                    f"missing source result for {source.value}"
                )
                continue

            if (
                source_result.status == ContextSourceStatus.AVAILABLE
                and source_result.value is None
            ):
                errors.append(
                    f"available source {source.value} has no value"
                )

            if (
                source_result.status == ContextSourceStatus.FAILED
                and source_result.error is None
            ):
                errors.append(
                    f"failed source {source.value} has no error"
                )

            context_value = getattr(
                result.context,
                source.value,
            )

            if (
                source_result.status == ContextSourceStatus.AVAILABLE
                and context_value is not source_result.value
            ):
                errors.append(
                    f"context value for {source.value} "
                    "does not match source result"
                )

            if (
                source_result.status
                in {
                    ContextSourceStatus.UNAVAILABLE,
                    ContextSourceStatus.FAILED,
                    ContextSourceStatus.NOT_REQUESTED,
                }
                and context_value is not None
            ):
                errors.append(
                    f"context contains unavailable source "
                    f"{source.value}"
                )

        return ContextValidation(
            valid=not errors,
            errors=tuple(errors),
        )