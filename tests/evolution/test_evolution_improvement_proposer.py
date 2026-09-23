import pytest

from brain.evolution.evolution_improvement_proposer import (
    EvolutionImprovementProposer,
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


def test_proposer_creates_proposal():
    proposer = EvolutionImprovementProposer()

    observation = _observation()

    proposal = proposer.propose(
        observation
    )

    assert isinstance(
        proposal,
        EvolutionImprovementProposal,
    )


def test_proposer_preserves_category():
    proposer = EvolutionImprovementProposer()

    observation = _observation(
        EvolutionImprovementCategory.VERIFICATION,
    )

    proposal = proposer.propose(
        observation
    )

    assert proposal.category is (
        EvolutionImprovementCategory.VERIFICATION
    )


def test_proposer_preserves_observation_as_evidence():
    proposer = EvolutionImprovementProposer()

    observation = _observation()

    proposal = proposer.propose(
        observation
    )

    assert proposal.evidence == (
        observation,
    )


def test_proposer_maps_verification_to_validator():
    proposer = EvolutionImprovementProposer()

    observation = _observation(
        EvolutionImprovementCategory.VERIFICATION,
    )

    proposal = proposer.propose(
        observation
    )

    assert proposal.target_component == (
        "evolution_validator"
    )


def test_proposer_maps_test_generation_to_test_generator():
    proposer = EvolutionImprovementProposer()

    observation = _observation(
        EvolutionImprovementCategory.TEST_GENERATION,
    )

    proposal = proposer.propose(
        observation
    )

    assert proposal.target_component == (
        "test_generator"
    )


def test_proposer_maps_orchestration_to_executor():
    proposer = EvolutionImprovementProposer()

    observation = _observation(
        EvolutionImprovementCategory.ORCHESTRATION,
    )

    proposal = proposer.propose(
        observation
    )

    assert proposal.target_component == (
        "evolution_executor"
    )


def test_proposal_contains_non_empty_problem():
    proposer = EvolutionImprovementProposer()

    proposal = proposer.propose(
        _observation()
    )

    assert proposal.problem


def test_proposal_contains_non_empty_improvement():
    proposer = EvolutionImprovementProposer()

    proposal = proposer.propose(
        _observation()
    )

    assert proposal.proposed_improvement


def test_proposal_contains_non_empty_expected_effect():
    proposer = EvolutionImprovementProposer()

    proposal = proposer.propose(
        _observation()
    )

    assert proposal.expected_effect


def test_proposer_rejects_invalid_observation():
    proposer = EvolutionImprovementProposer()

    with pytest.raises(
        TypeError,
        match=(
            "observation must be an "
            "EvolutionImprovementObservation"
        ),
    ):
        proposer.propose(
            None
        )


@pytest.mark.parametrize(
    (
        "category",
        "expected_target",
    ),
    (
        (
            EvolutionImprovementCategory.REQUIREMENT_UNDERSTANDING,
            "requirement_understanding",
        ),
        (
            EvolutionImprovementCategory.TASK_DECOMPOSITION,
            "task_decomposer",
        ),
        (
            EvolutionImprovementCategory.SYSTEM_DESIGN,
            "system_designer",
        ),
        (
            EvolutionImprovementCategory.ENGINEERING_PLANNING,
            "planner",
        ),
        (
            EvolutionImprovementCategory.CODE_GENERATION,
            "engineering_generation",
        ),
        (
            EvolutionImprovementCategory.TEST_GENERATION,
            "test_generator",
        ),
        (
            EvolutionImprovementCategory.VERIFICATION,
            "evolution_validator",
        ),
        (
            EvolutionImprovementCategory.DEBUGGING,
            "engineering_loop",
        ),
        (
            EvolutionImprovementCategory.REFACTORING,
            "engineering_loop",
        ),
        (
            EvolutionImprovementCategory.CAPABILITY_DISCOVERY,
            "capability_discovery",
        ),
        (
            EvolutionImprovementCategory.CAPABILITY_INTEGRATION,
            "capability_integrator",
        ),
        (
            EvolutionImprovementCategory.DEPENDENCY_MANAGEMENT,
            "dependency_management",
        ),
        (
            EvolutionImprovementCategory.SAFETY,
            "evolution_safety_policy",
        ),
        (
            EvolutionImprovementCategory.RECOVERY,
            "evolution_recovery",
        ),
        (
            EvolutionImprovementCategory.ORCHESTRATION,
            "evolution_executor",
        ),
    ),
)
def test_all_categories_have_target_components(
    category,
    expected_target,
):
    proposer = EvolutionImprovementProposer()

    proposal = proposer.propose(
        _observation(category)
    )

    assert proposal.target_component == (
        expected_target
    )