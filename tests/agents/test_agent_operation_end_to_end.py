
from brain.agents.agent_operation_coordinator import AgentOperationCoordinator
from brain.agents.agent_operation_restoration_coordinator import (
    AgentOperationRestorationCoordinator,
)
from brain.agents.agent_operation_workflow_coordinator import (
    AgentOperationWorkflowCoordinator,
)
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_lifecycle import AgentRuntimeLifecycleState
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
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
from brain.agents.workflow_coordinator import WorkflowCoordinator
from brain.agents.workflow_persistence import WorkflowPersistence
from brain.agents.goal_task_persistence import GoalTaskPersistence
from brain.capabilities.capability_executor import CapabilityExecutor
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.agents.persistence.json_agent_operation_persistence import (
    JsonAgentOperationPersistence,
)


class FakeGoalTaskPersistence:
    def __init__(self, state=None):
        self.state = state

    def save(self, state):
        self.state = state

    def load(self, agent_id):
        if self.state is None or self.state.agent_id != agent_id:
            raise KeyError(agent_id)
        return self.state


class FakeWorkflowPersistence:
    def __init__(self, state=None):
        self.state = state

    def save(self, state):
        self.state = state

    def load(self, workflow_id):
        if (
            self.state is None
            or self.state.workflow.id != workflow_id
        ):
            raise KeyError(workflow_id)
        return self.state


def create_runtime():
    definition = AgentDefinition(
        identity=AgentIdentity(id="agent-1", name="Test Agent"),
        description="Integration test agent",
        version="1.0",
        capabilities=frozenset(),
    )

    runtime = AgentRuntime(
        agent_definition=definition,
        capability_runtime=CapabilityRuntime(
            CapabilityExecutor(CapabilityRegistry())
        ),
        runtime_id="runtime-1",
    )
    runtime.transition_to(AgentRuntimeLifecycleState.READY)
    runtime.transition_to(AgentRuntimeLifecycleState.RUNNING)
    return runtime


def test_operation_survives_pause_restore_and_completes(tmp_path):
    runtime = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id="agent-1",
        description="Complete a two-step task",
        status=GoalStatus.ACTIVE,
    )

    tasks = (
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Complete the first step",
        ),
        AgentTask(
            id="task-2",
            goal_id="goal-1",
            description="Complete the second step",
            dependencies=frozenset({"task-1"}),
        ),
    )

    workflow = Workflow(
        id="workflow-1",
        goal_id="goal-1",
        step_ids=("step-1", "step-2"),
        status=WorkflowStatus.CREATED,
    )

    steps = (
        WorkflowStep(
            id="step-1",
            task_id="task-1",
            status=WorkflowStepStatus.PENDING,
        ),
        WorkflowStep(
            id="step-2",
            task_id="task-2",
            status=WorkflowStepStatus.PENDING,
        ),
    )

    operation = AgentOperation(
        id="operation-1",
        goal_id="goal-1",
        workflow_id="workflow-1",
        status=AgentOperationStatus.CREATED,
    )

    workflow_coordinator = WorkflowCoordinator()
    operation_coordinator = AgentOperationCoordinator()
    operation_workflow_coordinator = (
        AgentOperationWorkflowCoordinator()
    )

    # Initialize the workflow and start the operation.
    workflow, steps = workflow_coordinator.start(
        workflow, steps, tasks
    )
    operation = operation_coordinator.start(
        operation, goal, workflow
    )

    assert workflow.status is WorkflowStatus.RUNNING
    assert operation.status is AgentOperationStatus.RUNNING
    assert steps[0].status is WorkflowStepStatus.READY
    assert steps[1].status is WorkflowStepStatus.PENDING

    # Complete the first task.
    workflow, steps, tasks = (
        operation_workflow_coordinator.start_task_step(
            operation, runtime, goal, workflow, steps, tasks, "step-1"
        )
    )

    operation, workflow, steps, tasks = (
        operation_workflow_coordinator.complete_task_step(
            operation, runtime, goal, workflow, steps, tasks, "step-1"
        )
    )

    assert tasks[0].status is AgentTaskStatus.COMPLETED
    assert steps[0].status is WorkflowStepStatus.COMPLETED
    assert workflow.status is WorkflowStatus.RUNNING

    # Make the dependent second step ready.
    steps = operation_workflow_coordinator.refresh_ready_steps(
        operation, goal, workflow, steps, tasks
    )
    assert steps[1].status is WorkflowStepStatus.READY

    # Pause only at a safe boundary: no step is running.
    operation = operation_workflow_coordinator.pause(
        operation, goal, workflow, steps
    )
    assert operation.status is AgentOperationStatus.PAUSED

    # Persist the operation to disk and the other state through
    # their existing persistence contracts.
    operation_store = JsonAgentOperationPersistence(
        tmp_path / "operations"
    )
    goal_task_store = FakeGoalTaskPersistence()
    workflow_store = FakeWorkflowPersistence()

    operation_store.save(
        AgentOperationCheckpointState(operation=operation)
    )
    goal_task_store.save(
        GoalTaskPersistenceState(
            agent_id="agent-1",
            goals=(goal,),
            tasks=tasks,
        )
    )
    workflow_store.save(
        WorkflowPersistenceState(
            workflow=workflow,
            steps=steps,
        )
    )

    # Use a new operation persistence instance to read the disk checkpoint.
    restored_operation_store = JsonAgentOperationPersistence(
        tmp_path / "operations"
    )
    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=restored_operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    (
        restored_operation,
        restored_goal,
        restored_workflow,
        restored_steps,
        restored_tasks,
    ) = restoration.restore("operation-1", "agent-1")

    assert restored_operation.status is AgentOperationStatus.PAUSED
    assert restored_goal.id == "goal-1"
    assert restored_workflow.status is WorkflowStatus.RUNNING
    assert restored_steps[0].status is WorkflowStepStatus.COMPLETED
    assert restored_steps[1].status is WorkflowStepStatus.READY
    assert restored_tasks[0].status is AgentTaskStatus.COMPLETED
    assert restored_tasks[1].status is AgentTaskStatus.CREATED

    # Restoration validates state; it does not execute the next task.
    assert restored_steps[1].status is WorkflowStepStatus.READY
    assert restored_tasks[1].status is AgentTaskStatus.CREATED

    # Resume and complete the second task.
    restored_operation = operation_workflow_coordinator.resume(
        restored_operation, restored_goal, restored_workflow
    )

    (
        restored_workflow,
        restored_steps,
        restored_tasks,
    ) = operation_workflow_coordinator.start_task_step(
        restored_operation,
        runtime,
        restored_goal,
        restored_workflow,
        restored_steps,
        restored_tasks,
        "step-2",
    )

    (
        restored_operation,
        restored_workflow,
        restored_steps,
        restored_tasks,
    ) = operation_workflow_coordinator.complete_task_step(
        restored_operation,
        runtime,
        restored_goal,
        restored_workflow,
        restored_steps,
        restored_tasks,
        "step-2",
    )

    assert restored_tasks[1].status is AgentTaskStatus.COMPLETED
    assert restored_tasks[1].progress == 100
    assert all(
        step.status is WorkflowStepStatus.COMPLETED
        for step in restored_steps
    )
    assert restored_workflow.status is WorkflowStatus.COMPLETED
    assert restored_operation.status is AgentOperationStatus.COMPLETED
