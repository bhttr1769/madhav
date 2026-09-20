from brain.evolution.models.evolution_experience import EvolutionExperience


def test_evolution_experience_creation():
    experience = EvolutionExperience(
        evolution_id="evo-001",
        requested_capability="web_research",
        task_id="task-001",
        task_description="implement capability: web_research",
        outcome="success",
        lesson="Reuse the existing capability discovery mechanism.",
        reusable=True,
    )

    assert experience.evolution_id == "evo-001"
    assert experience.requested_capability == "web_research"
    assert experience.task_id == "task-001"
    assert experience.task_description == "implement capability: web_research"
    assert experience.outcome == "success"
    assert experience.lesson == "Reuse the existing capability discovery mechanism."
    assert experience.reusable is True


def test_evolution_experience_is_frozen():
    experience = EvolutionExperience(
        evolution_id="evo-001",
        requested_capability="web_research",
        task_id="task-001",
        task_description="implement capability: web_research",
        outcome="success",
        lesson="Reuse the existing capability discovery mechanism.",
        reusable=True,
    )

    try:
        experience.outcome = "failure"
    except AttributeError:
        pass
    else:
        raise AssertionError("EvolutionExperience must be immutable")