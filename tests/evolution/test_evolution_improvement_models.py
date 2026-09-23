import pytest

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)


def _observation():
    return EvolutionImprovementObservation(
        category=(
            EvolutionImprovementCategory.VERIFICATION
        ),
        description=(
            "Repeated verification failures"
        ),
        evolution_ids=(
            "evolution-1",
            "evolution-2",
        ),
        occurrence_count=2,
    )


def test_observation_can_be_created():
    observation = _observation()

    assert (
        observation.category
        is EvolutionImprovementCategory.VERIFICATION
    )

    assert observation.occurrence_count == 2


def test_observation_rejects_invalid_category():
    with pytest.raises(
        TypeError,
        match="category must be an",
    ):
        EvolutionImprovementObservation(
            category="verification",
            description="failure",
            evolution_ids=("evolution-1",),
            occurrence_count=1,
        )


def test_observation_rejects_empty_description():
    with pytest.raises(
        ValueError,
        match="description must not be empty",
    ):
        EvolutionImprovementObservation(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            description="",
            evolution_ids=("evolution-1",),
            occurrence_count=1,
        )


def test_observation_rejects_non_tuple_evolution_ids():
    with pytest.raises(
        TypeError,
        match="evolution_ids must be a tuple",
    ):
        EvolutionImprovementObservation(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            description="failure",
            evolution_ids=["evolution-1"],
            occurrence_count=1,
        )


def test_observation_rejects_empty_evolution_id():
    with pytest.raises(
        ValueError,
        match="evolution_ids must not contain",
    ):
        EvolutionImprovementObservation(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            description="failure",
            evolution_ids=("",),
            occurrence_count=1,
        )


def test_observation_rejects_invalid_occurrence_count():
    with pytest.raises(
        ValueError,
        match="occurrence_count must be at least 1",
    ):
        EvolutionImprovementObservation(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            description="failure",
            evolution_ids=(),
            occurrence_count=0,
        )


def test_observation_requires_matching_occurrence_count():
    with pytest.raises(
        ValueError,
        match="occurrence_count must match",
    ):
        EvolutionImprovementObservation(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            description="failure",
            evolution_ids=("evolution-1",),
            occurrence_count=2,
        )


def test_proposal_can_be_created():
    proposal = EvolutionImprovementProposal(
        category=(
            EvolutionImprovementCategory.VERIFICATION
        ),
        problem="Repeated verification failures",
        proposed_improvement=(
            "Improve verification-oriented "
            "test planning"
        ),
        evidence=(
            _observation(),
        ),
        target_component="test_generation",
        expected_effect=(
            "Reduce repeated verification failures"
        ),
    )

    assert (
        proposal.category
        is EvolutionImprovementCategory.VERIFICATION
    )

    assert proposal.evidence[0].occurrence_count == 2


def test_proposal_rejects_empty_evidence():
    with pytest.raises(
        ValueError,
        match="evidence must not be empty",
    ):
        EvolutionImprovementProposal(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            problem="Repeated verification failures",
            proposed_improvement="Improve verification",
            evidence=(),
            target_component="verification",
            expected_effect="Reduce failures",
        )


def test_proposal_rejects_invalid_evidence():
    with pytest.raises(
        TypeError,
        match="evidence must contain only",
    ):
        EvolutionImprovementProposal(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            problem="Repeated verification failures",
            proposed_improvement="Improve verification",
            evidence=("invalid",),
            target_component="verification",
            expected_effect="Reduce failures",
        )


def test_proposal_rejects_empty_target_component():
    with pytest.raises(
        ValueError,
        match="target_component must not be empty",
    ):
        EvolutionImprovementProposal(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            problem="Repeated verification failures",
            proposed_improvement="Improve verification",
            evidence=(_observation(),),
            target_component="",
            expected_effect="Reduce failures",
        )


def test_proposal_rejects_empty_expected_effect():
    with pytest.raises(
        ValueError,
        match="expected_effect must not be empty",
    ):
        EvolutionImprovementProposal(
            category=(
                EvolutionImprovementCategory.VERIFICATION
            ),
            problem="Repeated verification failures",
            proposed_improvement="Improve verification",
            evidence=(_observation(),),
            target_component="verification",
            expected_effect="",
        )