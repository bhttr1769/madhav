from dataclasses import FrozenInstanceError

import pytest

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


def requirement():

    return Requirement(
        original_request="Build an API",
        objective="Build an API",
        functional_requirements=frozenset({
            "The API must expose endpoints",
        }),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset({
            "The API responds successfully",
        }),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=1.0,
    )


def test_task_decomposition_preserves_task_order():

    task_a = Task(
        id="task-a",
        description="Inspect the backend",
        category="analysis",
        dependencies=frozenset(),
        affected_areas=frozenset({"backend"}),
        acceptance_criteria=frozenset(),
    )

    task_b = Task(
        id="task-b",
        description="Implement the API",
        category="implementation",
        dependencies=frozenset({"task-a"}),
        affected_areas=frozenset({"backend"}),
        acceptance_criteria=frozenset({
            "The API responds successfully",
        }),
    )

    decomposition = TaskDecomposition(
        requirement=requirement(),
        tasks=(task_a, task_b),
    )

    assert decomposition.tasks == (
        task_a,
        task_b,
    )

    assert decomposition.tasks[1].dependencies == frozenset({
        "task-a",
    })


def test_task_decomposition_is_immutable():

    decomposition = TaskDecomposition(
        requirement=requirement(),
        tasks=(),
    )

    with pytest.raises(FrozenInstanceError):
        decomposition.tasks = ()