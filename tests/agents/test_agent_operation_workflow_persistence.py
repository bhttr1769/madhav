
from unittest.mock import Mock

import pytest

from brain.agents.agent_operation_workflow_coordinator import (
    AgentOperationWorkflowCoordinator,
)
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
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


class RecordingOperationPersistence:
    def __init__(self, events, fail=False):
        self.events = events
        self.fail = fail
        self.state = None

    def save(self, state):
        self.events.append("operation")
        if self.fail:
            raise OSError("operation persistence failed")
        self.state = state

    def load(self, operation_id):
        if self.state is None:
            raise KeyError(operation_id)
        return self.state


class RecordingGoalTaskPersistence:
    def __init__(self, events, state=None, fail=False):
        self.events = events
        self.state = state
        self.fail = fail

    def save(self, state):
        self.events.append("goal_task")
        if self.fail:
            raise OSError("goal/task persistence failed")
        self.state = state

    def load(self, agent_id):
        if self.state is None or self.state.agent_id != agent_id:
            raise KeyError(agent_id)
        return self.state


class RecordingWorkflowPersistence:
    def __init__(self, events, fail=False):
        self.events = events
        self.fail = fail
        self.state = None

    def save(self, state):
        self.events.append("workflow")
        if self.fail:
            raise OSError("workflow persistence failed")
        self.state = state

    def load(self, workflow_id):
        if self.state is None:
            raise KeyError(workflow_id)
        return self.state


@pytest.fixture
def state():
    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Complete assigned work",
        status=GoalStatus.ACTIVE,
    )

    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Complete the task",
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

    return goal, (task,), workflow, steps, operation


def make_coordinator(events, fail_store=None, goal_task_state=None):
    operation_store = RecordingOperationPersistence(
        events,
        fail=fail_store == "operation",
    )
    goal_task_store = RecordingGoalTaskPersistence(
        events,
        state=goal_task_state,
        fail=fail_store == "goal_task",
    )
    workflow_store = RecordingWorkflowPersistence(
        events,
        fail=fail_store == "workflow",
    )

    coordinator = AgentOperationWorkflowCoordinator(
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    runtime = Mock()
    runtime.authorize_goal.return_value = None
    runtime.authorize_task.return_value = None

    return (
        coordinator,
        runtime,
        operation_store,
        goal_task_store,
        workflow_store,
    )


def complete_task(coordinator, runtime, state):
    goal, tasks, workflow, steps, operation = state

    return coordinator.complete_task_step(
        operation,
        runtime,
        goal,
        workflow,
        steps,
        tasks,
        "step-1",
    )


def test_saves_workflow_goal_tasks_then_operation(state):
    events = []
    coordinator, runtime, *_ = make_coordinator(events)

    updated_operation, updated_workflow, updated_steps, updated_tasks = (
        complete_task(coordinator, runtime, state)
    )

    assert events == ["workflow", "goal_task", "operation"]
    assert updated_workflow.status is WorkflowStatus.COMPLETED
    assert updated_steps[0].status is WorkflowStepStatus.COMPLETED
    assert updated_tasks[0].status is AgentTaskStatus.COMPLETED
    assert updated_operation.status is AgentOperationStatus.COMPLETED


@pytest.mark.parametrize(
    ("failed_store", "expected_events"),
    [
        ("workflow", ["workflow"]),
        ("goal_task", ["workflow", "goal_task"]),
        ("operation", ["workflow", "goal_task", "operation"]),
    ],
)
def test_persistence_failure_propagates_and_stops_later_saves(
    state,
    failed_store,
    expected_events,
):
    events = []
    coordinator, runtime, *_ = make_coordinator(
        events,
        fail_store=failed_store,
    )

    with pytest.raises(OSError, match="persistence failed"):
        complete_task(coordinator, runtime, state)

    assert events == expected_events


def test_goal_task_save_preserves_unrelated_goals_and_tasks(state):
    events = []

    other_goal = Goal(
        id="goal-2",
        agent_id="agent-1",
        description="Unrelated goal",
        status=GoalStatus.ACTIVE,
    )
    other_task = AgentTask(
        id="task-2",
        goal_id="goal-2",
        description="Unrelated task",
        status=AgentTaskStatus.CREATED,
    )

    initial_snapshot = GoalTaskPersistenceState(
        agent_id="agent-1",
        goals=(state[0], other_goal),
        tasks=(state[1][0], other_task),
    )

    (
        coordinator,
        runtime,
        _,
        goal_task_store,
        _,
    ) = make_coordinator(
        events,
        goal_task_state=initial_snapshot,
    )

    complete_task(coordinator, runtime, state)

    saved = goal_task_store.state

    assert {goal.id for goal in saved.goals} == {"goal-1", "goal-2"}
    assert {task.id for task in saved.tasks} == {"task-1", "task-2"}

    saved_tasks = {task.id: task for task in saved.tasks}
    assert saved_tasks["task-1"].status is AgentTaskStatus.COMPLETED
    assert saved_tasks["task-2"] == other_task


def test_partial_persistence_does_not_claim_rollback(state):
    events = []
    (
        coordinator,
        runtime,
        _,
        goal_task_store,
        workflow_store,
    ) = make_coordinator(events, fail_store="operation")

    with pytest.raises(OSError, match="operation persistence failed"):
        complete_task(coordinator, runtime, state)

    # Earlier independent writes succeeded; no cross-store rollback exists.
    assert workflow_store.state is not None
    assert goal_task_store.state is not None
    assert events == ["workflow", "goal_task", "operation"]


def test_persistence_dependencies_must_be_supplied_together():
    with pytest.raises(
        ValueError,
        match="all three persistence dependencies",
    ):
        AgentOperationWorkflowCoordinator(
            operation_persistence=RecordingOperationPersistence([]),
        )
