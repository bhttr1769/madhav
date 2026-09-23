import pytest

from brain.evolution.evolution_improvement_planner import (
    EvolutionImprovementPlanner,
)

from brain.evolution.evolution_improvement_request_builder import (
    EvolutionImprovementRequestBuilder,
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

from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


def _plan():
    observation = EvolutionImprovementObservation(
        category=(
            EvolutionImprovementCategory.VERIFICATION
        ),
        description=(
            "Repeated unsuccessful "
            "verification experiences."
        ),
        evolution_ids=(
            "evo-001",
            "evo-002",
        ),
        occurrence_count=2,
    )

    proposal = EvolutionImprovementProposal(
        category=(
            EvolutionImprovementCategory.VERIFICATION
        ),
        problem=(
            "Repeated unsuccessful verification "
            "experiences were observed."
        ),
        proposed_improvement=(
            "Review and improve the verification process."
        ),
        evidence=(
            observation,
        ),
        target_component="evolution_validator",
        expected_effect=(
            "Reduce repeated unsuccessful "
            "verification outcomes."
        ),
    )

    return EvolutionImprovementPlanner().plan(
        proposal
    )


def test_builder_creates_evolution_request():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan()
    )

    assert isinstance(
        request,
        EvolutionRequest,
    )


def test_builder_preserves_target_component():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan()
    )

    assert request.requested_capability == (
        "evolution_validator"
    )


def test_builder_includes_improvement_in_objective():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan()
    )

    assert (
        "Review and improve the verification process."
        in request.objective
    )


def test_builder_includes_problem_in_objective():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan()
    )

    assert (
        "Repeated unsuccessful verification "
        "experiences were observed."
        in request.objective
    )


def test_builder_includes_expected_effect():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan()
    )

    assert (
        "Reduce repeated unsuccessful "
        "verification outcomes."
        in request.objective
    )


def test_builder_preserves_plan_constraints():
    builder = EvolutionImprovementRequestBuilder()

    plan = _plan()

    request = builder.build(
        plan
    )

    for constraint in plan.constraints:
        assert constraint in request.constraints


def test_builder_defaults_to_supervised_mode():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan()
    )

    assert request.mode == "supervised"


def test_builder_accepts_explicit_mode():
    builder = EvolutionImprovementRequestBuilder()

    request = builder.build(
        _plan(),
        mode="proposal",
    )

    assert request.mode == "proposal"


def test_builder_rejects_invalid_plan():
    builder = EvolutionImprovementRequestBuilder()

    with pytest.raises(
        TypeError,
        match=(
            "plan must be an "
            "EvolutionImprovementPlan"
        ),
    ):
        builder.build(
            None
        )


def test_builder_rejects_invalid_mode():
    builder = EvolutionImprovementRequestBuilder()

    with pytest.raises(
        TypeError,
        match="mode must be a string",
    ):
        builder.build(
            _plan(),
            mode=None,
        )


def test_builder_rejects_empty_mode():
    builder = EvolutionImprovementRequestBuilder()

    with pytest.raises(
        ValueError,
        match="mode must not be empty",
    ):
        builder.build(
            _plan(),
            mode="",
        )