from brain.agents.agent_context_builder import AgentContextBuilder
from brain.agents.models.agent_context import AgentContext


def test_builder_creates_agent_context():
    builder = AgentContextBuilder()

    context = builder.build(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    assert isinstance(context, AgentContext)
    assert context.runtime_id == "runtime-1"
    assert context.agent_id == "agent-1"


def test_builder_integrates_existing_source_objects():
    builder = AgentContextBuilder()

    user = object()
    project = object()
    environment = object()
    memory = object()
    knowledge = object()
    perception = object()
    runtime = object()

    context = builder.build(
        runtime_id="runtime-1",
        agent_id="agent-1",
        user=user,
        project=project,
        environment=environment,
        memory=memory,
        knowledge=knowledge,
        perception=perception,
        runtime=runtime,
    )

    assert context.user is user
    assert context.project is project
    assert context.environment is environment
    assert context.memory is memory
    assert context.knowledge is knowledge
    assert context.perception is perception
    assert context.runtime is runtime


def test_builder_allows_partial_context():
    builder = AgentContextBuilder()

    project = object()

    context = builder.build(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=project,
    )

    assert context.project is project
    assert context.user is None
    assert context.environment is None
    assert context.memory is None
    assert context.knowledge is None
    assert context.perception is None
    assert context.runtime is None


def test_builder_does_not_modify_source_objects():
    builder = AgentContextBuilder()

    project = object()
    environment = object()

    context = builder.build(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=project,
        environment=environment,
    )

    assert context.project is project
    assert context.environment is environment


def test_builder_creates_independent_context_instances():
    builder = AgentContextBuilder()

    first = builder.build(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    second = builder.build(
        runtime_id="runtime-2",
        agent_id="agent-1",
    )

    assert first is not second
    assert first.runtime_id == "runtime-1"
    assert second.runtime_id == "runtime-2"