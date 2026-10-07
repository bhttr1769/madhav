from dataclasses import dataclass


@dataclass(frozen=True)
class AgentIdentity:
    id: str
    name: str