import pytest

from brain.evolution.evolution_experience_query import (
    EvolutionExperienceQuery,
)
from brain.evolution.evolution_experience_store import (
    EvolutionExperienceStore,
)
from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)


def _experience(
    evolution_id,
    capability,
    task_id,
    outcome,
    reusable,
):
    return EvolutionExperience(
        evolution_id=evolution_id,
        requested_capability=capability,
        task_id=task_id,
        task_description=f"task {task_id}",
        outcome=outcome,
        lesson=f"lesson {task_id}",
        reusable=reusable,
    )


@pytest.fixture
def query():
    store = EvolutionExperienceStore()

    store.add_all(
        (
            _experience(
                "evo-001",
                "web_research",
                "task-001",
                "success",
                True,
            ),
            _experience(
                "evo-001",
                "web_research",
                "task-002",
                "failure",
                True,
            ),
            _experience(
                "evo-002",
                "code_review",
                "task-003",
                "success",
                False,
            ),
        )
    )

    return EvolutionExperienceQuery(store)


def test_returns_all_experiences(query):
    experiences = query.all()

    assert len(experiences) == 3


def test_filters_by_capability(query):
    experiences = query.by_capability(
        "web_research"
    )

    assert len(experiences) == 2
    assert all(
        experience.requested_capability
        == "web_research"
        for experience in experiences
    )


def test_filters_by_evolution(query):
    experiences = query.by_evolution(
        "evo-001"
    )

    assert len(experiences) == 2
    assert all(
        experience.evolution_id == "evo-001"
        for experience in experiences
    )


def test_returns_reusable_experiences(query):
    experiences = query.reusable()

    assert len(experiences) == 2
    assert all(
        experience.reusable
        for experience in experiences
    )


def test_returns_successful_experiences(query):
    experiences = query.successful()

    assert len(experiences) == 2
    assert all(
        experience.outcome == "success"
        for experience in experiences
    )


def test_returns_failed_experiences(query):
    experiences = query.failed()

    assert len(experiences) == 1
    assert experiences[0].outcome == "failure"


def test_rejects_invalid_capability(query):
    with pytest.raises(TypeError):
        query.by_capability(None)


def test_rejects_empty_capability(query):
    with pytest.raises(ValueError):
        query.by_capability("")


def test_rejects_invalid_evolution_id(query):
    with pytest.raises(TypeError):
        query.by_evolution(None)


def test_rejects_empty_evolution_id(query):
    with pytest.raises(ValueError):
        query.by_evolution("")