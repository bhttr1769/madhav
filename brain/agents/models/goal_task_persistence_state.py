from dataclasses import dataclass

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal


@dataclass(frozen=True)
class GoalTaskPersistenceState:
    agent_id: str
    goals: tuple[Goal, ...]
    tasks: tuple[AgentTask, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        if not isinstance(self.goals, tuple):
            raise TypeError("goals must be a tuple")

        if not isinstance(self.tasks, tuple):
            raise TypeError("tasks must be a tuple")

        goal_ids = set()

        for goal in self.goals:
            if not isinstance(goal, Goal):
                raise TypeError(
                    "goals must contain Goal instances"
                )

            if goal.agent_id != self.agent_id:
                raise ValueError(
                    "goal agent_id must match persistence state agent_id"
                )

            if goal.id in goal_ids:
                raise ValueError(
                    f"duplicate goal ID: {goal.id}"
                )

            goal_ids.add(goal.id)

        task_ids = set()

        for task in self.tasks:
            if not isinstance(task, AgentTask):
                raise TypeError(
                    "tasks must contain AgentTask instances"
                )

            if task.goal_id not in goal_ids:
                raise ValueError(
                    f"task references unknown goal: {task.goal_id}"
                )

            if task.id in task_ids:
                raise ValueError(
                    f"duplicate task ID: {task.id}"
                )

            task_ids.add(task.id)