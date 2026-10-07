from dataclasses import dataclass

from brain.agents.models.agent_context import AgentContext
from brain.agents.models.context_source_result import ContextSourceResult


@dataclass(frozen=True)
class ContextIntegrationResult:
    context: AgentContext
    source_results: dict