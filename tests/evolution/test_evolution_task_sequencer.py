import pytest

from brain.engineering.tasks.models.task import (
    Task,
)
from brain.evolution.evolution_task_sequencer import (
    EvolutionTaskSequencer,
)


def create_task(
    task_id: str,
    description: str,
) -> Task:
    return Task(
        id=task_id,
        description=description,
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(),
        acceptance_criteria=(),
    )

def test_preserves_task_order():
    sequencer = EvolutionTaskSequencer()

    first = create_task(
        "task-1",
        "Implement file analysis.",
    )

    second = create_task(
        "task-2",
        "Implement repository analysis.",
    )

    third = create_task(
        "task-3",
        "Implement validation.",
    )

    result = sequencer.sequence(
        (
            first,
            second,
            third,
        )
    )

    assert result == (
        first,
        second,
        third,
    )


def test_returns_empty_for_no_tasks():
    sequencer = EvolutionTaskSequencer()

    result = sequencer.sequence(())

    assert result == ()


def test_rejects_non_tuple_tasks():
    sequencer = EvolutionTaskSequencer()

    with pytest.raises(
        TypeError,
        match="tasks must be a tuple",
    ):
        sequencer.sequence([])


def test_rejects_invalid_task():
    sequencer = EvolutionTaskSequencer()

    with pytest.raises(
        TypeError,
        match="Task instances",
    ):
        sequencer.sequence(
            ("invalid",)
        )