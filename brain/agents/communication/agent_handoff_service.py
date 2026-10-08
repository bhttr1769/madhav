from abc import ABC, abstractmethod

from brain.agents.models.agent_handoff import AgentHandoff


class AgentHandoffService(ABC):
    """
    Contract for coordinating agent task handoffs.

    This contract does not:
    - modify AgentTask
    - modify AgentAssignment
    - create agents
    - execute tasks
    - manage runtime lifecycle
    - bypass safety
    - persist handoffs
    """

    @abstractmethod
    def handoff(
        self,
        handoff: AgentHandoff,
    ) -> None:
        """
        Process an agent handoff request.
        """
        raise NotImplementedError