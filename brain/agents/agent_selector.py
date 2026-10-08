from brain.agents.agent_registry import AgentRegistry
from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_task import AgentTask


class AgentSelector:
    """
    Selects an existing registered agent for an AgentTask.

    Agent selection is based on explicitly supplied required
    capabilities. The selector does not create agents, modify
    the registry, execute tasks, or manage agent runtimes.
    """

    def __init__(self, registry: AgentRegistry) -> None:
        self._registry = registry

    def select(
        self,
        required_capabilities: frozenset[str],
    ) -> AgentDefinition:
        """
        Select the registered agent capable of satisfying all
        required capabilities.

        Exactly one matching agent must exist.

        Raises:
            TypeError: If required_capabilities is not a frozenset.
            ValueError: If capability IDs are invalid, no agent
                matches, or multiple agents match.
        """
        self._validate_required_capabilities(required_capabilities)

        candidates = tuple(
            agent
            for agent in self._registry.all()
            if required_capabilities.issubset(agent.capabilities)
        )

        if not candidates:
            raise ValueError(
                "No registered agent satisfies the required capabilities"
            )

        if len(candidates) > 1:
            raise ValueError(
                "Multiple registered agents satisfy the required capabilities"
            )

        return candidates[0]

    def delegate(
        self,
        task: AgentTask,
        required_capabilities: frozenset[str],
    ) -> AgentAssignment:
        """
        Select an agent for the supplied task and return an
        AgentAssignment.

        The task itself is not modified or executed.
        """
        if not isinstance(task, AgentTask):
            raise TypeError("task must be an AgentTask")

        agent = self.select(required_capabilities)

        return AgentAssignment(
            task_id=task.id,
            agent_id=agent.identity.id,
        )

    @staticmethod
    def _validate_required_capabilities(
        required_capabilities: frozenset[str],
    ) -> None:
        if not isinstance(required_capabilities, frozenset):
            raise TypeError(
                "required_capabilities must be a frozenset"
            )

        for capability_id in required_capabilities:
            if not isinstance(capability_id, str):
                raise TypeError(
                    "required_capabilities must contain only strings"
                )

            if not capability_id.strip():
                raise ValueError(
                    "required_capabilities must contain only "
                    "non-empty strings"
                )