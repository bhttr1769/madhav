from brain.evolution.evolution_experience_query import (
    EvolutionExperienceQuery,
)
from brain.evolution.evolution_experience_store import (
    EvolutionExperienceStore,
)
from brain.evolution.evolution_planner import (
    EvolutionPlanner,
)
from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)
from brain.evolution.models.evolution_plan import (
    EvolutionPlan,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)
from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)


def _request(
    capability="web_research",
):
    return EvolutionRequest(
        requested_capability=capability,
        objective="Add the requested capability.",
        constraints=frozenset(),
        mode="supervised",
    )


def _assessment(
    capability="web_research",
):
    return CapabilityAssessment(
        requested_capability=capability,
        available=False,
        status="unavailable",
        matched_capabilities=frozenset(),
        missing_capabilities=frozenset(
            {capability}
        ),
        rationale="Capability is not registered.",
    )


def _experience(
    evolution_id,
    capability,
    task_id,
    outcome,
):
    return EvolutionExperience(
        evolution_id=evolution_id,
        requested_capability=capability,
        task_id=task_id,
        task_description=(
            f"implement capability: {capability}"
        ),
        outcome=outcome,
        lesson=(
            f"Previous evolution {outcome}."
        ),
        reusable=True,
    )


def test_stored_experience_can_be_retrieved_for_planning():
    store = EvolutionExperienceStore()

    store.add(
        _experience(
            evolution_id="evo-001",
            capability="web_research",
            task_id="task-001",
            outcome="success",
        )
    )

    query = EvolutionExperienceQuery(store)

    experiences = query.by_capability(
        "web_research"
    )

    assert len(experiences) == 1
    assert experiences[0].evolution_id == "evo-001"


def test_retrieved_experience_can_be_supplied_to_evolution_planner():
    store = EvolutionExperienceStore()

    store.add(
        _experience(
            evolution_id="evo-001",
            capability="web_research",
            task_id="task-001",
            outcome="success",
        )
    )

    query = EvolutionExperienceQuery(store)

    experiences = query.by_capability(
        "web_research"
    )

    planner = EvolutionPlanner()

    plan = planner.plan(
        _request(),
        _assessment(),
        experiences=experiences,
    )

    assert isinstance(
        plan,
        EvolutionPlan,
    )

    assert plan.requested_capability == (
        "web_research"
    )

    assert plan.tasks == (
        "implement capability: web_research",
    )


def test_experience_for_another_capability_is_not_used():
    store = EvolutionExperienceStore()

    store.add(
        _experience(
            evolution_id="evo-001",
            capability="code_review",
            task_id="task-001",
            outcome="success",
        )
    )

    query = EvolutionExperienceQuery(store)

    experiences = query.by_capability(
        "web_research"
    )

    assert experiences == ()

    planner = EvolutionPlanner()

    plan = planner.plan(
        _request("web_research"),
        _assessment("web_research"),
        experiences=experiences,
    )

    assert plan.tasks == (
        "implement capability: web_research",
    )


def test_multiple_relevant_experiences_can_reach_planner():
    store = EvolutionExperienceStore()

    store.add_all(
        (
            _experience(
                evolution_id="evo-001",
                capability="web_research",
                task_id="task-001",
                outcome="success",
            ),
            _experience(
                evolution_id="evo-002",
                capability="web_research",
                task_id="task-002",
                outcome="failure",
            ),
        )
    )

    query = EvolutionExperienceQuery(store)

    experiences = query.by_capability(
        "web_research"
    )

    assert len(experiences) == 2

    planner = EvolutionPlanner()

    plan = planner.plan(
        _request(),
        _assessment(),
        experiences=experiences,
    )

    assert isinstance(
        plan,
        EvolutionPlan,
    )

    assert plan.tasks == (
        "implement capability: web_research",
    )