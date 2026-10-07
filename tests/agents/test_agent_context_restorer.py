import pytest

from brain.agents.agent_context_builder import AgentContextBuilder
from brain.agents.agent_context_integrator import AgentContextIntegrator
from brain.agents.agent_context_restorer import AgentContextRestorer
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.context_source import ContextSource
from brain.agents.context_source_coordinator import ContextSourceCoordinator
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.agents.models.context_restoration_state import (
    ContextRestorationState,
)
from brain.agents.models.context_source_result import (
    ContextSourceResult,
)
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
            output=request.input_data,
        )

class FakePersistence:
    def __init__(self, state):
        self.state = state

    def load(self, runtime_id):
        return self.state

    def save(self, state):
        self.state = state


class FakeProvider:
    def __init__(self, source, value):
        self.source = source
        self.value = value

    def provide(self):
        return ContextSourceResult(
            source=self.source,
            status=ContextSourceStatus.AVAILABLE,
            value=self.value,
        )


def create_runtime(agent_id="agent-1", runtime_id="runtime-1"):
    definition = AgentDefinition(
        identity=AgentIdentity(
            id=agent_id,
            name="Test Agent",
        ),
        description="Test agent definition",
        version="1.0.0",
        capabilities=frozenset(),
    )

    return AgentRuntime(
        definition,
        FakeCapabilityRuntime(),
        runtime_id=runtime_id,
    )


def create_restorer(state):
    integrator = AgentContextIntegrator(
        coordinator=ContextSourceCoordinator(),
        builder=AgentContextBuilder(),
    )

    return AgentContextRestorer(
        persistence=FakePersistence(state),
        integrator=integrator,
    )


def test_restorer_reconstructs_context_from_existing_providers():
    state = ContextRestorationState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        requested_sources=frozenset({
            ContextSource.PROJECT,
        }),
    )

    restorer = create_restorer(state)
    runtime = create_runtime()

    project = object()

    result = restorer.restore(
        runtime=runtime,
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
        ),
    )

    assert result.context.runtime is runtime
    assert result.context.runtime_id == runtime.runtime_id
    assert result.context.agent_id == runtime.agent_id
    assert result.context.project is project


def test_restorer_preserves_unavailable_source_status():
    state = ContextRestorationState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        requested_sources=frozenset({
            ContextSource.MEMORY,
        }),
    )

    restorer = create_restorer(state)
    runtime = create_runtime()

    result = restorer.restore(
        runtime=runtime,
        providers=(),
    )

    assert result.context.memory is None

    assert (
        result.source_results[ContextSource.MEMORY].status
        == ContextSourceStatus.UNAVAILABLE
    )


def test_restorer_rejects_persisted_runtime_mismatch():
    state = ContextRestorationState(
        runtime_id="runtime-2",
        agent_id="agent-1",
        requested_sources=frozenset(),
    )

    restorer = create_restorer(state)
    runtime = create_runtime(runtime_id="runtime-1")

    with pytest.raises(ValueError, match="runtime_id"):
        restorer.restore(
            runtime=runtime,
            providers=(),
        )


def test_restorer_rejects_persisted_agent_mismatch():
    state = ContextRestorationState(
        runtime_id="runtime-1",
        agent_id="agent-7",
        requested_sources=frozenset(),
    )

    restorer = create_restorer(state)
    runtime = create_runtime(agent_id="agent-1")

    with pytest.raises(ValueError, match="agent_id"):
        restorer.restore(
            runtime=runtime,
            providers=(),
        )