from abc import ABC, abstractmethod

from brain.agents.models.agent_plan import AgentPlan
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal


class AgentPlanner(ABC):
    """
    Contract for planning how an agent should accomplish a Goal
    using its existing AgentTasks.

    This contract produces an AgentPlan only.

    It does not:
    - create or modify Goals
    - create or modify AgentTasks
    - assign tasks to agents
    - select agents
    - execute capabilities
    - execute tasks
    - manage runtime lifecycle
    """

    @abstractmethod
    def plan(
        self,
        goal: Goal,
        tasks: tuple[AgentTask, ...],
    ) -> AgentPlan:
        """
        Create an agent-level plan for the supplied Goal and Tasks.

        Args:
            goal: The goal being planned.
            tasks: Existing AgentTasks belonging to the goal.

        Returns:
            An AgentPlan describing task ordering and planning strategy.

        Raises:
            ValueError: If the supplied tasks do not belong to the goal.
        """
        raise NotImplementedError