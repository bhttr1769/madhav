from brain.agents.models.agent_definition import (
    AgentDefinition,
)


class AgentRegistry:
    def __init__(
        self,
        agents: tuple[AgentDefinition, ...] = (),
    ):
        self._agents = {}

        for agent in agents:
            self.register(agent)

    def register(
        self,
        agent: AgentDefinition,
    ) -> None:
        if not isinstance(
            agent,
            AgentDefinition,
        ):
            raise TypeError(
                "agent must be an AgentDefinition"
            )

        agent_id = agent.identity.id

        if agent_id in self._agents:
            raise ValueError(
                f"agent already registered: {agent_id}"
            )

        self._agents[agent_id] = agent

    def get(
        self,
        agent_id: str,
    ) -> AgentDefinition:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise KeyError(
                f"agent not found: {agent_id}"
            ) from exc

    def has(
        self,
        agent_id: str,
    ) -> bool:
        return agent_id in self._agents

    def all(
        self,
    ) -> tuple[AgentDefinition, ...]:
        return tuple(
            self._agents.values()
        )

    def unregister(
        self,
        agent_id: str,
    ) -> None:
        if agent_id not in self._agents:
            raise KeyError(
                f"agent not found: {agent_id}"
            )

        del self._agents[agent_id]