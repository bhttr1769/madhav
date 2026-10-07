import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_lifecycle import AgentRuntimeLifecycleState
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


class FailingCapabilityRuntime(CapabilityRuntime):
    def __init__(self, error):
        self.error = error
        self.requests = []

    def execute(
        self,
        request: CapabilityExecutionRequest,
    ) -> CapabilityExecutionResult:
        self.requests.append(request)
        raise self.error


class FailedResultCapabilityRuntime(CapabilityRuntime):
    def __init__(self):
        self.requests = []

    def execute(
        self,
        request: CapabilityExecutionRequest,
    ) -> CapabilityExecutionResult:
        self.requests.append(request)

        return CapabilityExecutionResult(
            capability_id=request.capability_id,
            output=None,
            status="failed",
            error="capability execution failed",
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


def create_runtime(capability_runtime):
    return AgentRuntime(
        create_agent_definition(),
        capability_runtime,
        runtime_id="runtime-1",
    )


def start_runtime(runtime):
    runtime.transition_to(
        AgentRuntimeLifecycleState.READY
    )

    runtime.transition_to(
        AgentRuntimeLifecycleState.RUNNING
    )


def test_capability_runtime_exception_propagates():
    error = RuntimeError("capability failed")
    capability_runtime = FailingCapabilityRuntime(error)
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    with pytest.raises(RuntimeError, match="capability failed"):
        runtime.execute_capability(
            "test.execute",
            {"value": 1},
        )


def test_capability_runtime_exception_does_not_change_runtime_state():
    capability_runtime = FailingCapabilityRuntime(
        RuntimeError("capability failed")
    )
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    with pytest.raises(RuntimeError):
        runtime.execute_capability(
            "test.execute",
            {"value": 1},
        )

    assert runtime.state.state == AgentRuntimeLifecycleState.RUNNING.value


def test_capability_runtime_exception_does_not_change_runtime_identity():
    capability_runtime = FailingCapabilityRuntime(
        RuntimeError("capability failed")
    )
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    with pytest.raises(RuntimeError):
        runtime.execute_capability(
            "test.execute",
            {},
        )

    assert runtime.runtime_id == "runtime-1"
    assert runtime.agent_id == "agent-1"


def test_failed_capability_result_is_returned_without_runtime_verification():
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    result = runtime.execute_capability(
        "test.execute",
        {"value": 1},
    )

    assert result.status == "failed"
    assert result.error == "capability execution failed"
    assert result.capability_id == "test.execute"


def test_failed_capability_result_does_not_change_runtime_state():
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    runtime.execute_capability(
        "test.execute",
        {},
    )

    assert runtime.state.state == AgentRuntimeLifecycleState.RUNNING.value


def test_undeclared_capability_is_rejected_before_capability_runtime():
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    with pytest.raises(ValueError):
        runtime.execute_capability(
            "undeclared.capability",
            {},
        )

    assert capability_runtime.requests == []


def test_capability_is_rejected_when_runtime_is_not_running():
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    with pytest.raises(RuntimeError):
        runtime.execute_capability(
            "test.execute",
            {},
        )

    assert capability_runtime.requests == []


@pytest.mark.parametrize(
    "state",
    [
        AgentRuntimeLifecycleState.CREATED,
        AgentRuntimeLifecycleState.READY,
        AgentRuntimeLifecycleState.PAUSED,
        AgentRuntimeLifecycleState.STOPPED,
        AgentRuntimeLifecycleState.FAILED,
    ],
)
def test_capability_execution_is_rejected_outside_running_state(state):
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    if state != AgentRuntimeLifecycleState.CREATED:
        runtime.transition_to(
            AgentRuntimeLifecycleState.READY
        )

    if state == AgentRuntimeLifecycleState.PAUSED:
        runtime.transition_to(
            AgentRuntimeLifecycleState.RUNNING
        )
        runtime.transition_to(
            AgentRuntimeLifecycleState.PAUSED
        )

    elif state == AgentRuntimeLifecycleState.STOPPED:
        runtime.transition_to(
            AgentRuntimeLifecycleState.RUNNING
        )
        runtime.transition_to(
            AgentRuntimeLifecycleState.STOPPED
        )

    elif state == AgentRuntimeLifecycleState.FAILED:
        runtime.transition_to(
            AgentRuntimeLifecycleState.FAILED
        )

    with pytest.raises(RuntimeError):
        runtime.execute_capability(
            "test.execute",
            {},
        )

    assert capability_runtime.requests == []


def test_runtime_does_not_create_a_verification_result():
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    result = runtime.execute_capability(
        "test.execute",
        {},
    )

    assert isinstance(result, CapabilityExecutionResult)
    assert not hasattr(runtime, "verification")
    assert not hasattr(runtime, "_verification")


def test_runtime_does_not_replace_capability_failure_with_success():
    capability_runtime = FailedResultCapabilityRuntime()
    runtime = create_runtime(capability_runtime)

    start_runtime(runtime)

    result = runtime.execute_capability(
        "test.execute",
        {},
    )

    assert result.status == "failed"
    assert result.error is not None