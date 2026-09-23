import pytest

from brain.evolution.evolution_improvement_planner import (
    EvolutionImprovementPlanner,
)

from brain.evolution.evolution_improvement_request_builder import (
    EvolutionImprovementRequestBuilder,
)

from brain.evolution.evolution_executor import (
    EvolutionExecutor,
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

from brain.evolution.models.evolution_result import (
    EvolutionResult,
)


class FakeImprovementRequestBuilder:
    def __init__(
        self,
        request,
    ):
        self.request = request
        self.calls = []

    def build(
        self,
        plan,
        mode="supervised",
    ):
        self.calls.append(
            (
                plan,
                mode,
            )
        )

        return self.request


class FakeExecutor:
    def __init__(
        self,
    ):
        self.calls = []

        self.result = object()

    def execute(
        self,
        request,
        integration_request=None,
        dependency_signatures=None,
    ):
        self.calls.append(
            (
                request,
                integration_request,
                dependency_signatures,
            )
        )

        return self.result


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


def _executor(
    improvement_request_builder=None,
):
    return EvolutionExecutor(
        requirement_service=object(),
        task_decomposer=object(),
        system_designer=object(),
        planner=object(),
        engineering_generation=object(),
        test_generator=object(),
        engineering_loop=object(),
        existing_code=object(),
        verification_command="pytest tests -q",
        improvement_request_builder=(
            improvement_request_builder
        ),
    )


def test_executor_accepts_improvement_request_builder():
    builder = FakeImprovementRequestBuilder(
        request=object(),
    )

    executor = _executor(
        improvement_request_builder=builder,
    )

    assert executor._improvement_request_builder is builder


def test_execute_improvement_builds_evolution_request():
    builder = FakeImprovementRequestBuilder(
        request=object(),
    )

    executor = _executor(
        improvement_request_builder=builder,
    )

    plan = _plan()

    with pytest.raises(
        TypeError,
        match="request must be an EvolutionRequest",
    ):
        executor.execute_improvement(
            improvement_plan=plan,
        )

    assert len(builder.calls) == 1

    assert builder.calls[0][0] == plan

    assert builder.calls[0][1] == "supervised"


def test_execute_improvement_rejects_invalid_plan():
    executor = _executor()

    with pytest.raises(
        TypeError,
        match=(
            "plan must be an "
            "EvolutionImprovementPlan"
        ),
    ):
        executor.execute_improvement(
            improvement_plan=None,
        )


def test_execute_improvement_uses_requested_mode():
    builder = FakeImprovementRequestBuilder(
        request=object(),
    )

    executor = _executor(
        improvement_request_builder=builder,
    )

    plan = _plan()

    with pytest.raises(
        TypeError,
        match="request must be an EvolutionRequest",
    ):
        executor.execute_improvement(
            improvement_plan=plan,
            mode="proposal",
        )

    assert builder.calls[0][1] == "proposal"


def test_execute_improvement_preserves_dependency_inputs():
    builder = FakeImprovementRequestBuilder(
        request=object(),
    )

    executor = _executor(
        improvement_request_builder=builder,
    )

    plan = _plan()

    with pytest.raises(
        TypeError,
        match="request must be an EvolutionRequest",
    ):
        executor.execute_improvement(
            improvement_plan=plan,
            dependency_signatures="signatures",
        )

    assert len(builder.calls) == 1