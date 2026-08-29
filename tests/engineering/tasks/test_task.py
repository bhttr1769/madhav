from dataclasses import FrozenInstanceError

import pytest

from brain.engineering.tasks.models.task import (
    Task,
)


def test_task_can_be_created():

    task = Task(
        id="task-1",
        description="Implement authentication",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "authentication",
        }),
        acceptance_criteria=frozenset({
            "Users can authenticate",
        }),
    )

    assert task.id == "task-1"
    assert task.description == "Implement authentication"
    assert task.category == "implementation"


def test_task_is_immutable():

    task = Task(
        id="task-1",
        description="Implement authentication",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(),
        acceptance_criteria=frozenset(),
    )

    with pytest.raises(FrozenInstanceError):
        task.id = "task-2"