from dataclasses import dataclass


@dataclass(frozen=True)
class AgentContext:
    runtime_id: str
    agent_id: str
    user: object | None = None
    project: object | None = None
    environment: object | None = None
    memory: object | None = None
    knowledge: object | None = None
    perception: object | None = None
    runtime: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.runtime_id, str):
            raise TypeError("runtime_id must be a string")

        if not self.runtime_id.strip():
            raise ValueError("runtime_id must not be empty")

        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")