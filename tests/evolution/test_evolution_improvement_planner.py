import pytest

from brain.evolution.evolution_improvement_planner import (
    EvolutionImprovementPlanner,
)

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)

from brain.evolution.models.evolution_improvement_plan import (
    EvolutionImprovementPlan,
)


def _observation(
    category=EvolutionImprovementCategory.VERIFICATION,
):
    return EvolutionImprovementObservation(
        category=category,
        description=(
            "Repeated unsuccessful "
            f"{category.value} experiences."
        ),
        evolution_ids=(
            "evo-001",
            "evo-002",
        ),
        occurrence_count=2,
    )


def _proposal(
    category=EvolutionImprovementCategory.VERIFICATION,
):
    return EvolutionImprovementProposal(
        category=category,
        problem=(
            "Repeated unsuccessful "
            f"{category.value} experiences were observed."
        ),
        proposed_improvement=(
            "Review and improve the "
            f"{category.value} process."
        ),
        evidence=(
            _observation(category),
        ),
        target_component=(
            {
                EvolutionImprovementCategory.VERIFICATION:
                    "evolution_validator",
                EvolutionImprovementCategory.TEST_GENERATION:
                    "test_generator",
                EvolutionImprovementCategory.CODE_GENERATION:
                    "engineering_generation",
                EvolutionImprovementCategory.ORCHESTRATION:
                    "evolution_executor",
            }.get(
                category,
                "unknown",
            )
        ),
        expected_effect=(
            "Reduce repeated unsuccessful "
            f"{category.value} outcomes."
        ),
    )


def test_planner_creates_plan():
    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        _proposal()
    )

    assert isinstance(
        plan,
        EvolutionImprovementPlan,
    )


def test_planner_preserves_proposal():
    planner = EvolutionImprovementPlanner()

    proposal = _proposal()

    plan = planner.plan(
        proposal
    )

    assert plan.proposal == proposal


def test_planner_preserves_category():
    planner = EvolutionImprovementPlanner()

    proposal = _proposal(
        EvolutionImprovementCategory.TEST_GENERATION,
    )

    plan = planner.plan(
        proposal
    )

    assert plan.category is (
        EvolutionImprovementCategory.TEST_GENERATION
    )


def test_planner_preserves_target_component():
    planner = EvolutionImprovementPlanner()

    proposal = _proposal()

    plan = planner.plan(
        proposal
    )

    assert plan.target_component == (
        "evolution_validator"
    )


def test_planner_defines_implementation_direction():
    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        _proposal()
    )

    assert plan.implementation_direction


def test_planner_defines_reuse_strategy():
    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        _proposal()
    )

    assert plan.reuse_existing


def test_planner_defines_constraints():
    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        _proposal()
    )

    assert plan.constraints


def test_planner_defines_required_engineering_work():
    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        _proposal()
    )

    assert plan.required_engineering_work


def test_planner_rejects_invalid_proposal():
    planner = EvolutionImprovementPlanner()

    with pytest.raises(
        TypeError,
        match=(
            "proposal must be an "
            "EvolutionImprovementProposal"
        ),
    ):
        planner.plan(
            None
        )


@pytest.mark.parametrize(
    (
        "category",
        "expected_direction",
    ),
    (
        (
            EvolutionImprovementCategory.REQUIREMENT_UNDERSTANDING,
            "review and improve requirement understanding",
        ),
        (
            EvolutionImprovementCategory.TASK_DECOMPOSITION,
            "review and improve task decomposition",
        ),
        (
            EvolutionImprovementCategory.SYSTEM_DESIGN,
            "review and improve system design",
        ),
        (
            EvolutionImprovementCategory.ENGINEERING_PLANNING,
            "review and improve engineering planning",
        ),
        (
            EvolutionImprovementCategory.CODE_GENERATION,
            "review and improve code generation",
        ),
        (
            EvolutionImprovementCategory.TEST_GENERATION,
            "review and improve test generation",
        ),
        (
            EvolutionImprovementCategory.VERIFICATION,
            "review and improve verification",
        ),
        (
            EvolutionImprovementCategory.DEBUGGING,
            "review and improve debugging",
        ),
        (
            EvolutionImprovementCategory.REFACTORING,
            "review and improve refactoring",
        ),
        (
            EvolutionImprovementCategory.CAPABILITY_DISCOVERY,
            "review and improve capability discovery",
        ),
        (
            EvolutionImprovementCategory.CAPABILITY_INTEGRATION,
            "review and improve capability integration",
        ),
        (
            EvolutionImprovementCategory.DEPENDENCY_MANAGEMENT,
            "review and improve dependency management",
        ),
        (
            EvolutionImprovementCategory.SAFETY,
            "review and improve safety",
        ),
        (
            EvolutionImprovementCategory.RECOVERY,
            "review and improve recovery",
        ),
        (
            EvolutionImprovementCategory.ORCHESTRATION,
            "review and improve orchestration",
        ),
    ),
)
def test_planner_defines_category_specific_direction(
    category,
    expected_direction,
):
    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        _proposal(category)
    )

    assert plan.implementation_direction == (
        expected_direction
    )