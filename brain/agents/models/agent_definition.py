from dataclasses import dataclass

from brain.agents.models.agent_identity import AgentIdentity


@dataclass(frozen=True)
class AgentDefinition:
    identity: AgentIdentity
    description: str
    version: str
    capabilities: frozenset[str]