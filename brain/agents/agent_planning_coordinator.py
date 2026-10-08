from dataclasses import dataclass

from brain.agents.agent_selector import AgentSelector
from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_plan import AgentPlan
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal
from brain.agents.planning.agent_planner import AgentPlanner


@dataclass(frozen=True)
class AgentPlanningResult:
    """
    Result of planning and delegating a Goal.

    Contains the generated AgentPlan and the resulting
    task-to-agent assignments.
    """

    plan: AgentPlan
    assignments: tuple[AgentAssignment, ...]


class AgentPlanningCoordinator:
    """
    Coordinates planning and delegation.

    Responsibilities:
    - request an AgentPlan from AgentPlanner
    - resolve task-to-agent assignments using AgentSelector
    - return the combined result

    Does not:
    - execute tasks
    - execute capabilities
    - modify Goals or AgentTasks
    - manage AgentRuntime lifecycle
    - persist plans or assignments
    - create or modify agents
    """

    def __init__(
        self,
        planner: AgentPlanner,
        selector: AgentSelector,
    ) -> None:
        if not isinstance(planner, AgentPlanner):
            raise TypeError("planner must be an AgentPlanner")

        if not isinstance(selector, AgentSelector):
            raise TypeError("selector must be an AgentSelector")

        self._planner = planner
        self._selector = selector

    def plan_and_delegate(
        self,
        goal: Goal,
        tasks: tuple[AgentTask, ...],
        required_capabilities_by_task: dict[str, frozenset[str]],
    ) -> AgentPlanningResult:
        """
        Plan a Goal and delegate its tasks to suitable agents.

        Args:
            goal: Goal being planned.
            tasks: Existing AgentTasks belonging to the Goal.
            required_capabilities_by_task:
                Explicit capability requirements keyed by task ID.

        Returns:
            AgentPlanningResult containing the AgentPlan and assignments.
        """
        self._validate_tasks(tasks)
        self._validate_capability_requirements(
            required_capabilities_by_task
        )

        plan = self._planner.plan(
            goal,
            tasks,
        )

        task_by_id = {
            task.id: task
            for task in tasks
        }

        assignments: list[AgentAssignment] = []

        for task_id in plan.task_order:
            if task_id not in task_by_id:
                raise ValueError(
                    f"AgentPlan references unknown task: {task_id}"
                )

            required_capabilities = (
                required_capabilities_by_task.get(
                    task_id,
                    frozenset(),
                )
            )

            assignment = self._selector.delegate(
                task_by_id[task_id],
                required_capabilities,
            )

            assignments.append(assignment)

        return AgentPlanningResult(
            plan=plan,
            assignments=tuple(assignments),
        )

    @staticmethod
    def _validate_tasks(
        tasks: tuple[AgentTask, ...],
    ) -> None:
        if not isinstance(tasks, tuple):
            raise TypeError("tasks must be a tuple")

        for task in tasks:
            if not isinstance(task, AgentTask):
                raise TypeError(
                    "tasks must contain only AgentTask instances"
                )

    @staticmethod
    def _validate_capability_requirements(
        required_capabilities_by_task: dict[str, frozenset[str]],
    ) -> None:
        if not isinstance(required_capabilities_by_task, dict):
            raise TypeError(
                "required_capabilities_by_task must be a dict"
            )

        for task_id, capabilities in (
            required_capabilities_by_task.items()
        ):
            if not isinstance(task_id, str):
                raise TypeError(
                    "task capability mapping keys must be strings"
                )

            if not task_id.strip():
                raise ValueError(
                    "task capability mapping keys must be non-empty"
                )

            if not isinstance(capabilities, frozenset):
                raise TypeError(
                    "task capability requirements must be frozensets"
                )