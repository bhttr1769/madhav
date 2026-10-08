import pytest

from brain.agents.agent_registry import AgentRegistry
from brain.agents.agent_selector import AgentSelector
from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)
from brain.agents.models.agent_task import AgentTask


def create_agent(
    agent_id: str,
    capabilities: frozenset[str],
) -> AgentDefinition:
    return AgentDefinition(
        identity=AgentIdentity(
            id=agent_id,
            name=agent_id,
        ),
        description=f"Agent {agent_id}",
        version="1.0.0",
        capabilities=capabilities,
    )


def create_task(task_id: str = "task-1") -> AgentTask:
    return AgentTask(
        id=task_id,
        goal_id="goal-1",
        description="Complete the task",
    )


def test_selects_agent_with_required_capabilities() -> None:
    registry = AgentRegistry()

    agent = create_agent(
        "agent-1",
        frozenset({"coding", "testing"}),
    )

    registry.register(agent)

    selector = AgentSelector(registry)

    selected = selector.select(
        frozenset({"coding"}),
    )

    assert selected == agent


def test_agent_must_have_all_required_capabilities() -> None:
    registry = AgentRegistry()

    agent = create_agent(
        "agent-1",
        frozenset({"coding"}),
    )

    registry.register(agent)

    selector = AgentSelector(registry)

    with pytest.raises(
        ValueError,
        match="No registered agent",
    ):
        selector.select(
            frozenset({"coding", "testing"}),
        )


def test_rejects_when_no_agent_matches() -> None:
    registry = AgentRegistry()

    registry.register(
        create_agent(
            "agent-1",
            frozenset({"coding"}),
        )
    )

    selector = AgentSelector(registry)

    with pytest.raises(
        ValueError,
        match="No registered agent",
    ):
        selector.select(
            frozenset({"research"}),
        )


def test_rejects_ambiguous_selection() -> None:
    registry = AgentRegistry()

    registry.register(
        create_agent(
            "agent-1",
            frozenset({"coding"}),
        )
    )

    registry.register(
        create_agent(
            "agent-2",
            frozenset({"coding"}),
        )
    )

    selector = AgentSelector(registry)

    with pytest.raises(
        ValueError,
        match="Multiple registered agents",
    ):
        selector.select(
            frozenset({"coding"}),
        )


def test_accepts_empty_required_capabilities_when_one_agent_exists() -> None:
    registry = AgentRegistry()

    agent = create_agent(
        "agent-1",
        frozenset({"coding"}),
    )

    registry.register(agent)

    selector = AgentSelector(registry)

    selected = selector.select(frozenset())

    assert selected == agent


def test_rejects_non_frozenset_capabilities() -> None:
    registry = AgentRegistry()

    registry.register(
        create_agent(
            "agent-1",
            frozenset({"coding"}),
        )
    )

    selector = AgentSelector(registry)

    with pytest.raises(
        TypeError,
        match="frozenset",
    ):
        selector.select({"coding"})


def test_rejects_non_string_capability_id() -> None:
    registry = AgentRegistry()

    selector = AgentSelector(registry)

    with pytest.raises(
        TypeError,
        match="only strings",
    ):
        selector.select(
            frozenset({"coding", 123}),
        )


def test_rejects_empty_capability_id() -> None:
    registry = AgentRegistry()

    selector = AgentSelector(registry)

    with pytest.raises(
        ValueError,
        match="non-empty strings",
    ):
        selector.select(
            frozenset({"coding", ""}),
        )


def test_delegate_returns_agent_assignment() -> None:
    registry = AgentRegistry()

    agent = create_agent(
        "agent-1",
        frozenset({"coding"}),
    )

    registry.register(agent)

    selector = AgentSelector(registry)

    task = create_task()

    assignment = selector.delegate(
        task,
        frozenset({"coding"}),
    )

    assert isinstance(assignment, AgentAssignment)
    assert assignment.task_id == "task-1"
    assert assignment.agent_id == "agent-1"


def test_delegate_does_not_modify_task() -> None:
    registry = AgentRegistry()

    registry.register(
        create_agent(
            "agent-1",
            frozenset({"coding"}),
        )
    )

    selector = AgentSelector(registry)

    task = create_task()

    selector.delegate(
        task,
        frozenset({"coding"}),
    )

    assert task.id == "task-1"
    assert task.goal_id == "goal-1"
    assert task.description == "Complete the task"


def test_delegate_rejects_invalid_task() -> None:
    registry = AgentRegistry()

    registry.register(
        create_agent(
            "agent-1",
            frozenset({"coding"}),
        )
    )

    selector = AgentSelector(registry)

    with pytest.raises(
        TypeError,
        match="AgentTask",
    ):
        selector.delegate(
            "task-1",
            frozenset({"coding"}),
        )


def create_performance_record(
    agent_id: str,
    verified_successes: int,
    verified_failures: int,
) -> AgentPerformanceRecord:
    total = verified_successes + verified_failures

    return AgentPerformanceRecord(
        agent_id=agent_id,
        total_evaluations=total,
        successful_outcomes=verified_successes,
        unsuccessful_outcomes=verified_failures,
        inconclusive_outcomes=0,
        verified_successes=verified_successes,
        verified_failures=verified_failures,
    )


def test_selects_only_matching_agent_without_performance_data():
    first = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(agents=(first,))
    selector = AgentSelector(registry)

    result = selector.select(
        required_capabilities=frozenset({"coding"})
    )

    assert result == first


def test_multiple_matching_agents_remain_ambiguous_without_performance():
    first = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    second = create_agent(
        agent_id="agent-002",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(
        agents=(first, second)
    )

    selector = AgentSelector(registry)

    with pytest.raises(
        ValueError,
        match="Multiple registered agents",
    ):
        selector.select(
            required_capabilities=frozenset({"coding"})
        )

def test_selects_more_reliable_agent_when_multiple_agents_match():
    first = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    second = create_agent(
        agent_id="agent-002",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(
        agents=(first, second)
    )

    selector = AgentSelector(registry)

    records = (
        create_performance_record(
            agent_id="agent-001",
            verified_successes=8,
            verified_failures=2,
        ),
        create_performance_record(
            agent_id="agent-002",
            verified_successes=6,
            verified_failures=4,
        ),
    )

    result = selector.select(
        required_capabilities=frozenset({"coding"}),
        performance_records=records,
    )

    assert result == first


def test_missing_performance_record_does_not_break_single_match():
    agent = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(agents=(agent,))
    selector = AgentSelector(registry)

    result = selector.select(
        required_capabilities=frozenset({"coding"}),
        performance_records=(),
    )

    assert result == agent


def test_multiple_matches_with_incomplete_performance_data_remain_ambiguous():
    first = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    second = create_agent(
        agent_id="agent-002",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(
        agents=(first, second)
    )

    selector = AgentSelector(registry)

    records = (
        create_performance_record(
            agent_id="agent-001",
            verified_successes=8,
            verified_failures=2,
        ),
    )

    with pytest.raises(
        ValueError,
        match="performance data is incomplete",
    ):
        selector.select(
            required_capabilities=frozenset({"coding"}),
            performance_records=records,
        )


def test_equal_performance_remains_ambiguous():
    first = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    second = create_agent(
        agent_id="agent-002",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(
        agents=(first, second)
    )

    selector = AgentSelector(registry)

    records = (
        create_performance_record(
            agent_id="agent-001",
            verified_successes=8,
            verified_failures=2,
        ),
        create_performance_record(
            agent_id="agent-002",
            verified_successes=8,
            verified_failures=2,
        ),
    )

    with pytest.raises(
        ValueError,
        match="equal performance",
    ):
        selector.select(
            required_capabilities=frozenset({"coding"}),
            performance_records=records,
        )


def test_delegate_uses_performance_aware_selection():
    first = create_agent(
        agent_id="agent-001",
        capabilities=frozenset({"coding"}),
    )

    second = create_agent(
        agent_id="agent-002",
        capabilities=frozenset({"coding"}),
    )

    registry = AgentRegistry(
        agents=(first, second)
    )

    selector = AgentSelector(registry)

    task = AgentTask(
        id="task-001",
        goal_id="goal-001",
        description="Implement feature",
    )

    records = (
        create_performance_record(
            agent_id="agent-001",
            verified_successes=3,
            verified_failures=2,
        ),
        create_performance_record(
            agent_id="agent-002",
            verified_successes=9,
            verified_failures=1,
        ),
    )

    assignment = selector.delegate(
        task=task,
        required_capabilities=frozenset({"coding"}),
        performance_records=records,
    )

    assert assignment.task_id == "task-001"
    assert assignment.agent_id == "agent-002"