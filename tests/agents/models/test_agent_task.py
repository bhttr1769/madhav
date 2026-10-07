import pytest

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus


def test_agent_task_can_be_created():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    assert task.id == "task-1"
    assert task.goal_id == "goal-1"
    assert task.description == "Inspect the repository"


def test_agent_task_is_immutable():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    with pytest.raises(AttributeError):
        task.description = "Changed"


@pytest.mark.parametrize("field", ["id", "goal_id", "description"])
def test_agent_task_rejects_non_string_required_fields(field):
    values = {
        "id": "task-1",
        "goal_id": "goal-1",
        "description": "Inspect the repository",
    }
    values[field] = 123

    with pytest.raises(TypeError):
        AgentTask(**values)


@pytest.mark.parametrize("field", ["id", "goal_id", "description"])
def test_agent_task_rejects_empty_required_fields(field):
    values = {
        "id": "task-1",
        "goal_id": "goal-1",
        "description": "Inspect the repository",
    }
    values[field] = "   "

    with pytest.raises(ValueError):
        AgentTask(**values)


def test_agent_tasks_with_same_values_are_equal():
    first = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )
    second = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    assert first == second

def test_multiple_agent_tasks_can_reference_same_goal():
    first = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )
    second = AgentTask(
        id="task-2",
        goal_id="goal-1",
        description="Run the regression suite",
    )

    assert first.goal_id == "goal-1"
    assert second.goal_id == "goal-1"
    assert first.goal_id == second.goal_id

def test_agent_task_defaults_to_root_without_dependencies():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    assert task.parent_task_id is None
    assert task.dependencies == frozenset()


def test_agent_task_can_have_parent_task():
    task = AgentTask(
        id="task-2",
        goal_id="goal-1",
        description="Inspect the backend",
        parent_task_id="task-1",
    )

    assert task.parent_task_id == "task-1"


def test_agent_task_can_have_dependencies():
    task = AgentTask(
        id="task-3",
        goal_id="goal-1",
        description="Run tests",
        dependencies=frozenset({"task-1", "task-2"}),
    )

    assert task.dependencies == frozenset({"task-1", "task-2"})


def test_agent_task_rejects_self_parent():
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            parent_task_id="task-1",
        )


def test_agent_task_rejects_self_dependency():
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            dependencies=frozenset({"task-1"}),
        )


def test_agent_task_rejects_invalid_parent_task_id():
    with pytest.raises(TypeError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            parent_task_id=123,
        )


def test_agent_task_rejects_empty_parent_task_id():
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            parent_task_id="   ",
        )


def test_agent_task_rejects_non_frozenset_dependencies():
    with pytest.raises(TypeError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            dependencies={"task-2"},
        )


def test_agent_task_rejects_non_string_dependency_ids():
    with pytest.raises(TypeError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            dependencies=frozenset({"task-2", 123}),
        )


def test_agent_task_rejects_empty_dependency_ids():
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            dependencies=frozenset({"   "}),
        )

def test_agent_tasks_with_different_hierarchy_or_dependencies_are_not_equal():
    base = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    child = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
        parent_task_id="parent-1",
    )

    dependent = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
        dependencies=frozenset({"task-2"}),
    )

    assert base != child
    assert base != dependent

def test_agent_task_defaults_to_created_status():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    assert task.status is AgentTaskStatus.CREATED

def test_agent_task_accepts_explicit_status():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
        status=AgentTaskStatus.ACTIVE,
    )

    assert task.status is AgentTaskStatus.ACTIVE

def test_agent_task_rejects_invalid_status():
    with pytest.raises(TypeError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            status="active",
        )

def test_agent_task_defaults_to_zero_progress():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
    )

    assert task.progress == 0


def test_agent_task_accepts_valid_progress():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
        status=AgentTaskStatus.ACTIVE,
        progress=50,
    )

    assert task.progress == 50


@pytest.mark.parametrize("progress", [-1, 101])
def test_agent_task_rejects_progress_outside_range(progress):
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            progress=progress,
        )


def test_agent_task_rejects_non_integer_progress():
    with pytest.raises(TypeError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            progress=50.5,
        )


def test_agent_task_rejects_boolean_progress():
    with pytest.raises(TypeError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            progress=True,
        )


def test_completed_agent_task_requires_full_progress():
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            status=AgentTaskStatus.COMPLETED,
            progress=99,
        )


def test_completed_agent_task_accepts_full_progress():
    task = AgentTask(
        id="task-1",
        goal_id="goal-1",
        description="Inspect the repository",
        status=AgentTaskStatus.COMPLETED,
        progress=100,
    )

    assert task.progress == 100

@pytest.mark.parametrize(
    "status",
    [
        AgentTaskStatus.ACTIVE,
        AgentTaskStatus.FAILED,
        AgentTaskStatus.CANCELLED,
    ],
)
def test_non_completed_task_rejects_full_progress(status):
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            status=status,
            progress=100,
        )


def test_created_task_requires_zero_progress():
    with pytest.raises(ValueError):
        AgentTask(
            id="task-1",
            goal_id="goal-1",
            description="Inspect the repository",
            status=AgentTaskStatus.CREATED,
            progress=1,
        )