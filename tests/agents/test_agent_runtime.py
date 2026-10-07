import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_lifecycle import AgentRuntimeLifecycleState
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


class FakeCapabilityRuntime(CapabilityRuntime):
    def __init__(self):
        self.requests = []

    def execute(
        self,
        request: CapabilityExecutionRequest,
    ) -> CapabilityExecutionResult:
        self.requests.append(request)

        return CapabilityExecutionResult(
            capability_id=request.capability_id,
            output={
                "input": request.input_data,
            },
        )


def create_agent_definition():
    return AgentDefinition(
        identity=AgentIdentity(
            id="agent-1",
            name="Test Agent",
        ),
        description="Test agent definition",
        version="1.0.0",
        capabilities=frozenset(
            {
                "test.execute",
            }
        ),
    )


def create_runtime():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
        runtime_id="runtime-1",
    )

    return runtime, capability_runtime


def test_agent_runtime_stores_agent_definition():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    assert runtime.agent_definition is definition


def test_agent_runtime_generates_runtime_id():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    assert isinstance(runtime.runtime_id, str)
    assert runtime.runtime_id


def test_agent_runtime_accepts_explicit_runtime_id():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
        runtime_id="runtime-1",
    )

    assert runtime.runtime_id == "runtime-1"


def test_agent_runtime_starts_in_created_state():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    assert runtime.state.state == AgentRuntimeLifecycleState.CREATED.value


def test_agent_runtime_state_contains_agent_identity():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    assert runtime.state.agent_id == "agent-1"
    assert runtime.agent_id == "agent-1"


def test_agent_runtime_can_transition_state():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    result = runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    assert result.state == AgentRuntimeLifecycleState.READY.value
    assert runtime.state.state == AgentRuntimeLifecycleState.READY.value


def test_agent_runtime_preserves_runtime_id_across_transitions():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
        runtime_id="runtime-1",
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    assert runtime.runtime_id == "runtime-1"


def test_agent_runtime_preserves_agent_id_across_transitions():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    assert runtime.agent_id == "agent-1"
    assert runtime.state.agent_id == "agent-1"


def test_agent_runtime_rejects_invalid_agent_definition():
    capability_runtime = FakeCapabilityRuntime()

    with pytest.raises(TypeError):
        AgentRuntime(
            "invalid",
            capability_runtime,
        )


def test_agent_runtime_rejects_invalid_capability_runtime():
    definition = create_agent_definition()

    with pytest.raises(TypeError):
        AgentRuntime(
            definition,
            object(),
        )


@pytest.mark.parametrize("runtime_id", ["", "   "])
def test_agent_runtime_rejects_empty_runtime_id(runtime_id):
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    with pytest.raises(ValueError):
        AgentRuntime(
            definition,
            capability_runtime,
            runtime_id=runtime_id,
        )


def test_agent_runtime_rejects_non_string_runtime_id():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    with pytest.raises(TypeError):
        AgentRuntime(
            definition,
            capability_runtime,
            runtime_id=123,
        )


def test_agent_runtime_rejects_invalid_transition():
    definition = create_agent_definition()
    capability_runtime = FakeCapabilityRuntime()

    runtime = AgentRuntime(
        definition,
        capability_runtime,
    )

    with pytest.raises(ValueError):
        runtime.transition_to(
            AgentRuntimeLifecycleState.RUNNING
        )


def test_agent_runtime_executes_associated_capability():
    runtime, capability_runtime = create_runtime()

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    result = runtime.execute_capability(
        "test.execute",
        {"value": 42},
    )

    assert result.capability_id == "test.execute"
    assert result.output == {
        "input": {"value": 42},
    }

    assert len(capability_runtime.requests) == 1

    request = capability_runtime.requests[0]

    assert request.capability_id == "test.execute"
    assert request.input_data == {"value": 42}


def test_agent_runtime_does_not_execute_capability_before_running():
    runtime, capability_runtime = create_runtime()

    with pytest.raises(RuntimeError):
        runtime.execute_capability(
            "test.execute",
            {"value": 42},
        )

    assert capability_runtime.requests == []


def test_agent_runtime_rejects_unassociated_capability():
    runtime, capability_runtime = create_runtime()

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    with pytest.raises(ValueError):
        runtime.execute_capability(
            "unknown.capability",
            {},
        )

    assert capability_runtime.requests == []


def test_agent_runtime_rejects_empty_capability_id():
    runtime, capability_runtime = create_runtime()

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    with pytest.raises(ValueError):
        runtime.execute_capability(
            "",
            {},
        )

    assert capability_runtime.requests == []


def test_agent_runtime_rejects_non_string_capability_id():
    runtime, capability_runtime = create_runtime()

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    with pytest.raises(TypeError):
        runtime.execute_capability(
            123,
            {},
        )

    assert capability_runtime.requests == []


def test_agent_runtime_does_not_mutate_state_during_capability_execution():
    runtime, _ = create_runtime()

    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )

    runtime.execute_capability(
        "test.execute",
        {},
    )

    assert runtime.state.state == AgentRuntimeLifecycleState.RUNNING.value


def test_multiple_runtimes_are_independent():
    definition = create_agent_definition()

    runtime_one = AgentRuntime(
        definition,
        FakeCapabilityRuntime(),
        runtime_id="runtime-1",
    )

    runtime_two = AgentRuntime(
        definition,
        FakeCapabilityRuntime(),
        runtime_id="runtime-2",
    )

    runtime_one.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    assert runtime_one.runtime_id != runtime_two.runtime_id
    assert runtime_one.state.state == AgentRuntimeLifecycleState.READY.value
    assert runtime_two.state.state == AgentRuntimeLifecycleState.CREATED.value


def test_runtime_can_operate_on_owned_goal():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id=runtime.agent_id,
        description="Prepare the project",
    )

    assert runtime.can_operate_on_goal(goal)


def test_runtime_rejects_goal_owned_by_another_agent():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id="different-agent",
        description="Prepare the project",
    )

    assert not runtime.can_operate_on_goal(goal)


def test_runtime_authorizes_owned_goal():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id=runtime.agent_id,
        description="Prepare the project",
    )

    runtime.authorize_goal(goal)


def test_runtime_rejects_unauthorized_goal():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id="different-agent",
        description="Prepare the project",
    )

    with pytest.raises(ValueError):
        runtime.authorize_goal(goal)


def test_runtime_can_operate_on_task_through_owned_goal():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id=runtime.agent_id,
        description="Prepare the project",
    )

    task = AgentTask(
        id="task-1",
        goal_id=goal.id,
        description="Inspect the repository",
    )

    assert runtime.can_operate_on_task(task, goal)


def test_runtime_rejects_task_from_different_goal():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id=runtime.agent_id,
        description="Prepare the project",
    )

    task = AgentTask(
        id="task-1",
        goal_id="different-goal",
        description="Inspect the repository",
    )

    assert not runtime.can_operate_on_task(task, goal)


def test_runtime_rejects_task_through_goal_owned_by_another_agent():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id="different-agent",
        description="Prepare the project",
    )

    task = AgentTask(
        id="task-1",
        goal_id=goal.id,
        description="Inspect the repository",
    )

    assert not runtime.can_operate_on_task(task, goal)


def test_runtime_authorizes_owned_task():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id=runtime.agent_id,
        description="Prepare the project",
    )

    task = AgentTask(
        id="task-1",
        goal_id=goal.id,
        description="Inspect the repository",
    )

    runtime.authorize_task(task, goal)


def test_runtime_rejects_unauthorized_task():
    runtime, _ = create_runtime()

    goal = Goal(
        id="goal-1",
        agent_id="different-agent",
        description="Prepare the project",
    )

    task = AgentTask(
        id="task-1",
        goal_id=goal.id,
        description="Inspect the repository",
    )

    with pytest.raises(ValueError):
        runtime.authorize_task(task, goal)