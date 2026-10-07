from dataclasses import dataclass

from brain.agents.context_source import ContextSource


@dataclass(frozen=True)
class ContextRestorationState:
    runtime_id: str
    agent_id: str
    requested_sources: frozenset[ContextSource]

    def __post_init__(self) -> None:
        if not isinstance(self.runtime_id, str):
            raise TypeError("runtime_id must be a string")

        if not self.runtime_id.strip():
            raise ValueError("runtime_id must not be empty")

        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        if not isinstance(self.requested_sources, frozenset):
            raise TypeError(
                "requested_sources must be a frozenset"
            )

        for source in self.requested_sources:
            if not isinstance(source, ContextSource):
                raise TypeError(
                    "requested_sources must contain only ContextSource values"
                )