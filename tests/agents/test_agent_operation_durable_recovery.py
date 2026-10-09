import pytest
from brain.agents.agent_operation_coordinator import AgentOperationCoordinator
from brain.agents.agent_operation_restoration_coordinator import (
    AgentOperationRestorationCoordinator,
)
from brain.agents.agent_operation_workflow_coordinator import (
    AgentOperationWorkflowCoordinator,
)
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_lifecycle import AgentRuntimeLifecycleState
from brain.agents.goal_task_persistence import GoalTaskPersistence
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
from brain.agents.persistence.json_agent_operation_persistence import (
    JsonAgentOperationPersistence,
)
from brain.agents.persistence.json_goal_task_persistence import (
    JsonGoalTaskPersistence,
)
from brain.agents.persistence.json_workflow_persistence import (
    JsonWorkflowPersistence,
)
from brain.agents.workflow_coordinator import WorkflowCoordinator


def create_runtime():
    definition = AgentDefinition(
        identity=AgentIdentity(id="agent-1", name="Test Agent"),
        description="Durable recovery test agent",
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


from brain.capabilities.capability_executor import CapabilityExecutor
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.capability_runtime import CapabilityRuntime


def create_persistence_stores(root):
    return (
        JsonAgentOperationPersistence(root / "operations"),
        JsonGoalTaskPersistence(root / "goals-and-tasks"),
        JsonWorkflowPersistence(root / "workflows"),
    )


def test_operation_survives_real_json_restart_and_completes(tmp_path):
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

    operation_store, goal_task_store, workflow_store = (
        create_persistence_stores(tmp_path)
    )

    coordinator = AgentOperationWorkflowCoordinator(
        operation_coordinator=operation_coordinator,
        workflow_coordinator=workflow_coordinator,
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    # Initialize the workflow and start the operation.
    workflow, steps = workflow_coordinator.start(
        workflow,
        steps,
        tasks,
    )
    operation = operation_coordinator.start(
        operation,
        goal,
        workflow,
    )

    # Complete the first task.
    workflow, steps, tasks = coordinator.start_task_step(
        operation,
        runtime,
        goal,
        workflow,
        steps,
        tasks,
        "step-1",
    )

    (
        operation,
        workflow,
        steps,
        tasks,
    ) = coordinator.complete_task_step(
        operation,
        runtime,
        goal,
        workflow,
        steps,
        tasks,
        "step-1",
    )

    assert tasks[0].status is AgentTaskStatus.COMPLETED
    assert steps[0].status is WorkflowStepStatus.COMPLETED

    # Make the dependent step ready and pause at a safe boundary.
    steps = coordinator.refresh_ready_steps(
        operation,
        goal,
        workflow,
        steps,
        tasks,
    )

    assert steps[1].status is WorkflowStepStatus.READY

    operation = coordinator.pause(
        operation,
        goal,
        workflow,
        steps,
    )
    assert operation.status is AgentOperationStatus.PAUSED

    # Simulate a process restart by creating new store instances.
    (
        restored_operation_store,
        restored_goal_task_store,
        restored_workflow_store,
    ) = create_persistence_stores(tmp_path)

    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=restored_operation_store,
        goal_task_persistence=restored_goal_task_store,
        workflow_persistence=restored_workflow_store,
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

    # Restoration must not execute the next task.
    assert restored_steps[1].status is WorkflowStepStatus.READY
    assert restored_tasks[1].status is AgentTaskStatus.CREATED

    # Resume explicitly, then complete the second task.
    restored_operation = coordinator.resume(
        restored_operation,
        restored_goal,
        restored_workflow,
    )

    (
        restored_workflow,
        restored_steps,
        restored_tasks,
    ) = coordinator.start_task_step(
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
    ) = coordinator.complete_task_step(
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


def test_recovery_rejects_partial_write_when_final_operation_save_fails(
    tmp_path, monkeypatch
):
    runtime = create_runtime()

    goal = Goal(
        id="goal-partial",
        agent_id="agent-1",
        description="Test partial persistence failure",
        status=GoalStatus.ACTIVE,
    )
    task = AgentTask(
        id="task-partial",
        goal_id=goal.id,
        description="Complete the final task",
        status=AgentTaskStatus.ACTIVE,
    )
    workflow = Workflow(
        id="workflow-partial",
        goal_id=goal.id,
        step_ids=("step-partial",),
        status=WorkflowStatus.RUNNING,
    )
    steps = (
        WorkflowStep(
            id="step-partial",
            task_id=task.id,
            status=WorkflowStepStatus.RUNNING,
        ),
    )
    operation = AgentOperation(
        id="operation-partial",
        goal_id=goal.id,
        workflow_id=workflow.id,
        status=AgentOperationStatus.RUNNING,
    )

    operation_store, goal_task_store, workflow_store = (
        create_persistence_stores(tmp_path)
    )

    # Seed the last known persisted state.
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
        WorkflowPersistenceState(workflow=workflow, steps=steps)
    )

    coordinator = AgentOperationWorkflowCoordinator(
        operation_coordinator=AgentOperationCoordinator(),
        workflow_coordinator=WorkflowCoordinator(),
        operation_persistence=operation_store,
        goal_task_persistence=goal_task_store,
        workflow_persistence=workflow_store,
    )

    # Simulate failure at the final write, after workflow and task saves.
    def fail_operation_save(_state):
        raise OSError("simulated operation checkpoint write failure")

    monkeypatch.setattr(operation_store, "save", fail_operation_save)

    with pytest.raises(OSError, match="simulated operation checkpoint"):
        coordinator.complete_task_step(
            operation,
            runtime,
            goal,
            workflow,
            steps,
            (task,),
            "step-partial",
        )

    # Earlier independent writes remain; no multi-store rollback exists.
    persisted_workflow = workflow_store.load(workflow.id)
    persisted_goal_tasks = goal_task_store.load(goal.agent_id)

    assert persisted_workflow.workflow.status is WorkflowStatus.COMPLETED
    assert (
        persisted_goal_tasks.tasks[0].status
        is AgentTaskStatus.COMPLETED
    )

    # A fresh restoration coordinator must reject the inconsistent snapshot.
    (
        restored_operation_store,
        restored_goal_task_store,
        restored_workflow_store,
    ) = create_persistence_stores(tmp_path)

    restoration = AgentOperationRestorationCoordinator(
        operation_persistence=restored_operation_store,
        goal_task_persistence=restored_goal_task_store,
        workflow_persistence=restored_workflow_store,
    )

    with pytest.raises(
        ValueError,
        match="active or paused operation requires a RUNNING workflow",
    ):
        restoration.restore(operation.id, goal.agent_id)

