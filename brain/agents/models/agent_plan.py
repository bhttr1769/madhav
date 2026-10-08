from dataclasses import dataclass


@dataclass(frozen=True)
class AgentPlan:
    """
    Represents an agent-level plan for accomplishing a Goal.

    The plan references existing AgentTask IDs rather than storing
    or duplicating AgentTask objects.
    """

    goal_id: str
    task_order: tuple[str, ...]
    strategy: tuple[str, ...]
    confidence: float

    def __post_init__(self) -> None:
        if not isinstance(self.goal_id, str):
            raise TypeError("goal_id must be a string")

        if not self.goal_id.strip():
            raise ValueError("goal_id must be a non-empty string")

        if not isinstance(self.task_order, tuple):
            raise TypeError("task_order must be a tuple")

        for task_id in self.task_order:
            if not isinstance(task_id, str):
                raise TypeError("task_order must contain only strings")

            if not task_id.strip():
                raise ValueError(
                    "task_order must contain only non-empty strings"
                )

        if len(self.task_order) != len(set(self.task_order)):
            raise ValueError(
                "task_order must not contain duplicate task IDs"
            )

        if not isinstance(self.strategy, tuple):
            raise TypeError("strategy must be a tuple")

        for step in self.strategy:
            if not isinstance(step, str):
                raise TypeError("strategy must contain only strings")

            if not step.strip():
                raise ValueError(
                    "strategy must contain only non-empty strings"
                )

        if isinstance(self.confidence, bool):
            raise TypeError("confidence must be a number")

        if not isinstance(self.confidence, (int, float)):
            raise TypeError("confidence must be a number")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0"
            )