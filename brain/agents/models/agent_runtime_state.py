from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRuntimeState:
    runtime_id: str
    agent_id: str
    state: str

    def __post_init__(self):
        if not isinstance(self.runtime_id, str):
            raise TypeError("runtime_id must be a string")

        if not self.runtime_id.strip():
            raise ValueError("runtime_id must not be empty")

        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        if not isinstance(self.state, str):
            raise TypeError("state must be a string")

        if not self.state.strip():
            raise ValueError("state must not be empty")