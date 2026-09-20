import pytest

from brain.evolution.evolution_experience_store import (
    EvolutionExperienceStore,
)
from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)


def _experience(
    evolution_id="evo-001",
    task_id="task-001",
):
    return EvolutionExperience(
        evolution_id=evolution_id,
        requested_capability="web_research",
        task_id=task_id,
        task_description="implement capability",
        outcome="success",
        lesson="Capability implementation succeeded.",
        reusable=True,
    )


def test_adds_experience():
    store = EvolutionExperienceStore()

    experience = _experience()

    store.add(experience)

    assert store.all() == (experience,)


def test_adds_multiple_experiences():
    store = EvolutionExperienceStore()

    first = _experience(
        evolution_id="evo-001",
        task_id="task-001",
    )
    second = _experience(
        evolution_id="evo-002",
        task_id="task-002",
    )

    store.add_all((first, second))

    assert store.all() == (first, second)


def test_empty_store_returns_empty_tuple():
    store = EvolutionExperienceStore()

    assert store.all() == ()


def test_rejects_invalid_experience():
    store = EvolutionExperienceStore()

    with pytest.raises(TypeError):
        store.add(None)


def test_rejects_non_tuple_experiences():
    store = EvolutionExperienceStore()

    with pytest.raises(TypeError):
        store.add_all([])


def test_store_returns_immutable_view():
    store = EvolutionExperienceStore()

    experience = _experience()
    store.add(experience)

    experiences = store.all()

    assert isinstance(experiences, tuple)
    assert experiences == (experience,)