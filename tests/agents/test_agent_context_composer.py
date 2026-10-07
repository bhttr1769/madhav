import pytest

from brain.agents.agent_context_composer import AgentContextComposer
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.models.agent_context import AgentContext
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
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


def create_runtime(
    runtime_id="runtime-1",
    agent_id="agent-1",
):
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


def test_composer_preserves_same_runtime_reference():
    composer = AgentContextComposer()

    runtime = create_runtime()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    result = composer.compose(base, update)

    assert result.runtime is runtime


def test_composer_rejects_different_runtime_objects():
    composer = AgentContextComposer()

    base_runtime = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    update_runtime = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=base_runtime,
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=update_runtime,
    )

    with pytest.raises(ValueError, match="same AgentRuntime"):
        composer.compose(base, update)


def test_composer_rejects_runtime_identity_mismatch():
    composer = AgentContextComposer()

    runtime = create_runtime(
        runtime_id="runtime-2",
        agent_id="agent-1",
    )

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    with pytest.raises(ValueError, match="runtime_id"):
        composer.compose(base, update)


def test_composer_rejects_non_runtime_object():
    composer = AgentContextComposer()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=object(),
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    with pytest.raises(ValueError, match="AgentRuntime"):
        composer.compose(base, update)


def test_composer_preserves_existing_context():
    composer = AgentContextComposer()

    project = object()
    environment = object()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=project,
        environment=environment,
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    result = composer.compose(base, update)

    assert result is not base
    assert result.project is project
    assert result.environment is environment


def test_composer_applies_new_context_values():
    composer = AgentContextComposer()

    old_project = object()
    new_project = object()
    new_environment = object()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=old_project,
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=new_project,
        environment=new_environment,
    )

    result = composer.compose(base, update)

    assert result.project is new_project
    assert result.environment is new_environment


def test_composer_preserves_runtime_and_agent_identity():
    composer = AgentContextComposer()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    result = composer.compose(base, update)

    assert result.runtime_id == "runtime-1"
    assert result.agent_id == "agent-1"


def test_composer_rejects_different_runtime():
    composer = AgentContextComposer()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    update = AgentContext(
        runtime_id="runtime-2",
        agent_id="agent-1",
    )

    with pytest.raises(ValueError, match="runtime_id"):
        composer.compose(base, update)


def test_composer_rejects_different_agent():
    composer = AgentContextComposer()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-2",
    )

    with pytest.raises(ValueError, match="agent_id"):
        composer.compose(base, update)


def test_composer_does_not_mutate_contexts():
    composer = AgentContextComposer()

    base_project = object()
    update_project = object()

    base = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=base_project,
    )

    update = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=update_project,
    )

    result = composer.compose(base, update)

    assert base.project is base_project
    assert update.project is update_project
    assert result.project is update_project