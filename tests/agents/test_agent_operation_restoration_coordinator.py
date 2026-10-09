
import pytest

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
from brain.agents.models.goal import Goal, GoalStatus
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
from brain.agents.persistence.agent_operation_persistence import (
    AgentOperationPersistence,
)


class FakeOperationPersistence(AgentOperationPersistence):
    def __init__(self, state):
        self.state = state

    def save(self, state):
        self.state = state

    def load(self, operation_id):
        if self.state.operation.id != operation_id:
            raise KeyError(operation_id)
        return self.state


class FakeGoalTaskPersistence:
    def __init__(self, state):
        self.state = state
        self.load_calls = []

    def save(self, state):
        self.state = state

    def load(self, agent_id):
        self.load_calls.append(agent_id)
        if self.state.agent_id != agent_id:
            raise KeyError(agent_id)
        return self.state


class FakeWorkflowPersistence:
    def __init__(self, state):
        self.state = state
        self.load_calls = []

    def save(self, state):
        self.state = state

    def load(self, workflow_id):
        self.load_calls.append(workflow_id)
        if self.state.workflow.id != workflow_id:
            raise KeyError(workflow_id)
        return self.state


@pytest.fixture
def valid_state():
    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.PAUSED,
    )
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Complete a task",
        status=GoalStatus.ACTIVE,
    )
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Perform work",
        status=AgentTaskStatus.ACTIVE,
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1",),
        status=WorkflowStatus.RUNNING,
    )
    step = WorkflowStep(
        id="step-1",
        task_id="task-1",
        status=WorkflowStepStatus.READY,
    )

    return operation, goal, task, workflow, step


@pytest.fixture
def persistence(valid_state):
    operation, goal, task, workflow, step = valid_state

    operation_store = FakeOperationPersistence(
        AgentOperationCheckpointState(operation=operation)
    )
    goal_task_store = FakeGoalTaskPersistence(
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(goal,),
            tasks=(task,),
        )
    )
    workflow_store = FakeWorkflowPersistence(
        WorkflowPersistenceState(
            workflow=workflow,
            steps=(step,),
        )
    )

    return operation_store, goal_task_store, workflow_store


@pytest.fixture
def coordinator(persistence):
    return AgentOperationRestorationCoordinator(
        operation_persistence=persistence[0],
        goal_task_persistence=persistence[1],
        workflow_persistence=persistence[2],
    )


def test_restore_returns_valid_state_without_mutating_it(
    coordinator,
    valid_state,
):
    operation, goal, task, workflow, step = valid_state

    restored = coordinator.restore("operation-1", "agent-1")

    assert restored == (
        operation,
        goal,
        workflow,
        (step,),
        (task,),
    )
    assert restored[0].status is AgentOperationStatus.PAUSED
    assert restored[2].status is WorkflowStatus.RUNNING


def test_restore_rejects_missing_operation(coordinator, persistence):
    with pytest.raises(KeyError):
        coordinator.restore("missing-operation", "agent-1")


def test_restore_rejects_missing_goal(coordinator, persistence):
    persistence[1].state = GoalTaskPersistenceState(
        agent_id="agent-1",
        goals=(),
        tasks=(),
    )

    with pytest.raises(ValueError, match="persisted goal not found"):
        coordinator.restore("operation-1", "agent-1")


def test_restore_rejects_missing_workflow(coordinator, persistence):
    persistence[2].state = WorkflowPersistenceState(
        workflow=Workflow(
            id="different-workflow",
            goal_id="goal-1",
            step_ids=("step-1",),
            status=WorkflowStatus.RUNNING,
        ),
        steps=(
            WorkflowStep(
                id="step-1",
                task_id="task-1",
                status=WorkflowStepStatus.READY,
            ),
        ),
    )

    with pytest.raises(KeyError):
        coordinator.restore("operation-1", "agent-1")


def test_restore_rejects_workflow_id_mismatch(
    coordinator,
    persistence,
):
    persistence[2].state = WorkflowPersistenceState(
        workflow=Workflow(
            id="workflow-1",
            goal_id="different-goal",
            step_ids=("step-1",),
            status=WorkflowStatus.RUNNING,
        ),
        steps=(
            WorkflowStep(
                id="step-1",
                task_id="task-1",
                status=WorkflowStepStatus.READY,
            ),
        ),
    )

    with pytest.raises(ValueError, match="workflow goal_id"):
        coordinator.restore("operation-1", "agent-1")


def test_restore_rejects_step_referencing_unknown_task(
    coordinator,
    persistence,
):
    persistence[2].state = WorkflowPersistenceState(
        workflow=persistence[2].state.workflow,
        steps=(
            WorkflowStep(
                id="step-1",
                task_id="missing-task",
                status=WorkflowStepStatus.READY,
            ),
        ),
    )

    with pytest.raises(ValueError, match="unknown task"):
        coordinator.restore("operation-1", "agent-1")



def test_restore_rejects_task_from_another_goal(
    coordinator,
    persistence,
):
    persistence[1].state = GoalTaskPersistenceState(
        agent_id="agent-1",
        goals=(
            Goal(
                id="goal-1",
                agent_id="agent-1",
                description="Operation goal",
                status=GoalStatus.ACTIVE,
            ),
            Goal(
                id="goal-2",
                agent_id="agent-1",
                description="Another goal",
                status=GoalStatus.ACTIVE,
            ),
        ),
        tasks=(
            AgentTask(
                id="task-1",
                goal_id="goal-2",
                description="Task belonging to another goal",
                status=AgentTaskStatus.ACTIVE,
            ),
        ),
    )

    with pytest.raises(ValueError, match="another goal"):
        coordinator.restore("operation-1", "agent-1")



def test_restore_rejects_running_step_for_paused_operation(
    coordinator,
    persistence,
):
    persistence[2].state = WorkflowPersistenceState(
        workflow=persistence[2].state.workflow,
        steps=(
            WorkflowStep(
                id="step-1",
                task_id="task-1",
                status=WorkflowStepStatus.RUNNING,
            ),
        ),
    )

    with pytest.raises(ValueError, match="interrupted RUNNING step"):
        coordinator.restore("operation-1", "agent-1")


@pytest.mark.parametrize(
    ("operation_status", "workflow_status"),
    [
        (AgentOperationStatus.COMPLETED, WorkflowStatus.RUNNING),
        (AgentOperationStatus.FAILED, WorkflowStatus.COMPLETED),
        (AgentOperationStatus.RUNNING, WorkflowStatus.COMPLETED),
    ],
)
def test_restore_rejects_inconsistent_lifecycle(
    coordinator,
    persistence,
    valid_state,
    operation_status,
    workflow_status,
):
    operation, _, _, workflow, step = valid_state

    persistence[0].state = AgentOperationCheckpointState(
        operation=AgentOperation(
            id=operation.id,
            goal_id=operation.goal_id,
            workflow_id=operation.workflow_id,
            status=operation_status,
        )
    )
    persistence[2].state = WorkflowPersistenceState(
        workflow=Workflow(
            id=workflow.id,
            goal_id=workflow.goal_id,
            step_ids=workflow.step_ids,
            status=workflow_status,
        ),
        steps=(step,),
    )

    with pytest.raises(ValueError):
        coordinator.restore("operation-1", "agent-1")


def test_restore_rejects_completed_step_with_incomplete_task(
    coordinator,
    persistence,
):
    persistence[2].state = WorkflowPersistenceState(
        workflow=persistence[2].state.workflow,
        steps=(
            WorkflowStep(
                id="step-1",
                task_id="task-1",
                status=WorkflowStepStatus.COMPLETED,
            ),
        ),
    )

    with pytest.raises(ValueError, match="non-completed task"):
        coordinator.restore("operation-1", "agent-1")


def test_restore_rejects_failed_step_with_nonfailed_task(
    coordinator,
    persistence,
    valid_state,
):
    operation, _, _, workflow, _ = valid_state

    persistence[0].state = AgentOperationCheckpointState(
        operation=AgentOperation(
            id=operation.id,
            goal_id=operation.goal_id,
            workflow_id=operation.workflow_id,
            status=AgentOperationStatus.FAILED,
        )
    )
    persistence[1].state = GoalTaskPersistenceState(
        agent_id="agent-1",
        goals=(
            Goal(
                id="goal-1",
                agent_id="agent-1",
                description="Complete a task",
                status=GoalStatus.ACTIVE,
            ),
        ),
        tasks=(
            AgentTask(
                id="task-1",
                goal_id="goal-1",
                description="Perform work",
                status=AgentTaskStatus.ACTIVE,
            ),
        ),
    )
    persistence[2].state = WorkflowPersistenceState(
        workflow=Workflow(
            id=workflow.id,
            goal_id=workflow.goal_id,
            step_ids=workflow.step_ids,
            status=WorkflowStatus.FAILED,
        ),
        steps=(
            WorkflowStep(
                id="step-1",
                task_id="task-1",
                status=WorkflowStepStatus.FAILED,
            ),
        ),
    )

    with pytest.raises(ValueError, match="non-failed task"):
        coordinator.restore("operation-1", "agent-1")


def test_restore_rejects_wrong_agent_id(coordinator):
    with pytest.raises(KeyError):
        coordinator.restore("operation-1", "different-agent")


def test_restore_uses_existing_persistence_contracts(
    coordinator,
    persistence,
):
    coordinator.restore("operation-1", "agent-1")

    assert persistence[1].load_calls == ["agent-1"]
    assert persistence[2].load_calls == ["workflow-1"]
