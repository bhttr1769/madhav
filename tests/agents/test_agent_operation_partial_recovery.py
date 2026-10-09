
import pytest

from brain.agents.agent_operation_coordinator import AgentOperationCoordinator
from brain.agents.agent_operation_restoration_coordinator import (
    AgentOperationRestorationCoordinator,
)
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.goal_task_persistence_state import (
    GoalTaskPersistenceState,
)
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_persistence_state import (
    WorkflowPersistenceState,
)
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.persistence.json_agent_operation_persistence import (
    JsonAgentOperationPersistence,
)
from brain.agents.persistence.json_goal_task_persistence import (
    JsonGoalTaskPersistence,
)
from brain.agents.persistence.json_workflow_persistence import (
    JsonWorkflowPersistence,
)


def create_state():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Recovery test",
        status=GoalStatus.ACTIVE,
    )
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="First task",
        status=AgentTaskStatus.ACTIVE,
        progress=50,
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.RUNNING,
    )
    steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.RUNNING,
        ),
    )
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.RUNNING,
    )
    return goal, task, workflow, steps, operation


def create_stores(tmp_path):
    return (
        JsonAgentOperationPersistence(tmp_path / "operations"),
        JsonGoalTaskPersistence(tmp_path / "goals"),
        JsonWorkflowPersistence(tmp_path / "workflows"),
    )


def save_state(stores, goal, task, workflow, steps, operation):
    operation_store, goal_task_store, workflow_store = stores

    operation_store.save(
        AgentOperationCheckpointState(operation=operation)
    )
    goal_task_store.save(
        GoalTaskPersistenceState(
            agent_id=goal.agent_id,
            goals=(goal,),
            tasks=(task,),
        )
    )
    workflow_store.save(
        WorkflowPersistenceState(
            workflow=workflow,
            steps=steps,
        )
    )


def test_restore_rejects_interrupted_running_step(tmp_path):
    goal, task, workflow, steps, operation = create_state()
    stores = create_stores(tmp_path)
    save_state(stores, goal, task, workflow, steps, operation)

    operation_store, goal_task_store, workflow_store = create_stores(
        tmp_path
    )
    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    with pytest.raises(
        ValueError,
        match="interrupted RUNNING step",
    ):
        restoration.restore("operation-1", "agent-1")


def test_restore_rejects_completed_step_with_active_task(tmp_path):
    goal, task, workflow, _, operation = create_state()
    completed_steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.COMPLETED,
        ),
    )
    stores = create_stores(tmp_path)
    save_state(
        stores,
        goal,
        task,
        workflow,
        completed_steps,
        operation,
    )

    operation_store, goal_task_store, workflow_store = create_stores(
        tmp_path
    )
    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    with pytest.raises(
        ValueError,
        match="completed step has a non-completed task",
    ):
        restoration.restore("operation-1", "agent-1")


def test_restore_rejects_failed_step_with_active_task(tmp_path):
    goal, task, workflow, _, operation = create_state()
    failed_workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.FAILED,
    )
    failed_operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.FAILED,
    )
    failed_steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.FAILED,
        ),
    )
    stores = create_stores(tmp_path)
    save_state(
        stores,
        goal,
        task,
        failed_workflow,
        failed_steps,
        failed_operation,
    )

    operation_store, goal_task_store, workflow_store = create_stores(
        tmp_path
    )
    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    with pytest.raises(
        ValueError,
        match="failed step has a non-failed task",
    ):
        restoration.restore("operation-1", "agent-1")


def test_restore_rejects_completed_operation_with_running_workflow(
    tmp_path,
):
    goal, task, workflow, steps, _ = create_state()
    completed_operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.COMPLETED,
    )
    stores = create_stores(tmp_path)
    save_state(
        stores,
        goal,
        task,
        workflow,
        steps,
        completed_operation,
    )

    operation_store, goal_task_store, workflow_store = create_stores(
        tmp_path
    )
    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    with pytest.raises(
        ValueError,
        match="COMPLETED operation requires a COMPLETED workflow",
    ):
        restoration.restore("operation-1", "agent-1")

def test_restore_preserves_cancelled_operation_state(tmp_path):
    goal, task, workflow, steps, operation = create_state()

    cancelled_operation = AgentOperation(
        id=operation.id,
        goal_id=operation.goal_id,
        workflow_id=operation.workflow_id,
        status=AgentOperationStatus.CANCELLED,
    )

    stores = create_stores(tmp_path)
    save_state(
        stores,
        goal,
        task,
        workflow,
        steps,
        cancelled_operation,
    )

    operation_store, goal_task_store, workflow_store = create_stores(tmp_path)
    restoration = AgentOperationRestorationCoordinator(
        operation_store,
        goal_task_store,
        workflow_store,
    )

    restored_operation, restored_goal, restored_workflow, restored_steps, restored_tasks = (
        restoration.restore("operation-1", "agent-1")
    )

    assert restored_operation.status is AgentOperationStatus.CANCELLED
    assert restored_workflow.status is WorkflowStatus.RUNNING
    assert restored_steps[0].status is WorkflowStepStatus.RUNNING
    assert restored_tasks[0].status is AgentTaskStatus.ACTIVE
