from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.workflow import Workflow
from brain.agents.models.workflow_step import WorkflowStep, WorkflowStepStatus


class WorkflowTaskIntegration:
    """Coordinates workflow-step readiness with existing AgentTask state."""

    def validate(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
    ) -> None:
        if not isinstance(workflow, Workflow):
            raise TypeError("workflow must be a Workflow")

        if not isinstance(steps, tuple):
            raise TypeError("steps must be a tuple")

        if not isinstance(tasks, tuple):
            raise TypeError("tasks must be a tuple")

        step_ids = [step.id for step in steps]

        if len(step_ids) != len(set(step_ids)):
            raise ValueError("workflow step IDs must be unique")

        task_ids = [task.id for task in tasks]

        if len(task_ids) != len(set(task_ids)):
            raise ValueError("task IDs must be unique")

        workflow_step_ids = set(workflow.step_ids)
        provided_step_ids = set(step_ids)

        if provided_step_ids != workflow_step_ids:
            raise ValueError(
                "provided steps must exactly match workflow step IDs"
            )

        task_by_id = {
            task.id: task
            for task in tasks
        }

        for step in steps:
            if not isinstance(step, WorkflowStep):
                raise TypeError(
                    "all steps must be WorkflowStep instances"
                )

            task = task_by_id.get(step.task_id)

            if task is None:
                raise ValueError(
                    "workflow step references an unknown task"
                )

            if task.goal_id != workflow.goal_id:
                raise ValueError(
                    "workflow step task must belong to workflow goal"
                )

        for task in tasks:
            if not isinstance(task, AgentTask):
                raise TypeError(
                    "all tasks must be AgentTask instances"
                )

            unknown_dependencies = (
                task.dependencies - set(task_ids)
            )

            if unknown_dependencies:
                raise ValueError(
                    "task contains unknown dependency references"
                )

            if task.goal_id != workflow.goal_id:
                raise ValueError(
                    "task must belong to workflow goal"
                )

    def ready_steps(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
    ) -> tuple[WorkflowStep, ...]:
        self.validate(
            workflow,
            steps,
            tasks,
        )

        task_by_id = {
            task.id: task
            for task in tasks
        }

        ready: list[WorkflowStep] = []

        for step in steps:
            if step.status is not WorkflowStepStatus.PENDING:
                continue

            task = task_by_id[step.task_id]

            dependencies_completed = all(
                task_by_id[dependency_id].status
                is AgentTaskStatus.COMPLETED
                for dependency_id in task.dependencies
            )

            if dependencies_completed:
                ready.append(step)

        return tuple(ready)