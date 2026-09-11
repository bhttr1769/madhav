import pytest

from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.evolution.evolution_planner import (
    EvolutionPlanner,
)
from brain.evolution.models.evolution_plan import (
    EvolutionPlan,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
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


def _missing_assessment(
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


def _available_assessment(
    capability="web_research",
):
    return CapabilityAssessment(
        requested_capability=capability,
        available=True,
        status="available",
        matched_capabilities=frozenset(
            {capability}
        ),
        missing_capabilities=frozenset(),
        rationale="Capability is registered.",
    )


def test_planner_creates_plan_for_missing_capability():
    request = _request()
    assessment = _missing_assessment()

    plan = EvolutionPlanner().plan(
        request,
        assessment,
    )

    assert isinstance(
        plan,
        EvolutionPlan,
    )

    assert plan.requested_capability == (
        "web_research"
    )

    assert plan.current_status == "missing"

    assert plan.required_capabilities == (
        frozenset({"web_research"})
    )

    assert plan.tasks == (
        "analyze capability requirements",
        "design capability architecture",
        "implement capability",
        "generate tests",
        "review implementation",
        "verify implementation",
    )


def test_planner_includes_validation_strategy():
    plan = EvolutionPlanner().plan(
        _request(),
        _missing_assessment(),
    )

    assert plan.validation_strategy == (
        "run generated tests",
        "run existing engineering tests",
        "verify capability integration",
    )


def test_planner_includes_risks():
    plan = EvolutionPlanner().plan(
        _request(),
        _missing_assessment(),
    )

    assert plan.risks == frozenset(
        {"implementation may fail verification"}
    )


def test_planner_handles_existing_capability():
    plan = EvolutionPlanner().plan(
        _request(),
        _available_assessment(),
    )

    assert plan.current_status == (
        "already_available"
    )

    assert plan.reusable_capabilities == (
        frozenset({"web_research"})
    )

    assert plan.required_capabilities == frozenset()
    assert plan.tasks == ()
    assert plan.risks == frozenset()


def test_planner_rejects_invalid_request():
    with pytest.raises(TypeError):
        EvolutionPlanner().plan(
            None,
            _missing_assessment(),
        )


def test_planner_rejects_invalid_assessment():
    with pytest.raises(TypeError):
        EvolutionPlanner().plan(
            _request(),
            None,
        )


def test_planner_rejects_mismatched_capability():
    with pytest.raises(ValueError):
        EvolutionPlanner().plan(
            _request("web_research"),
            _missing_assessment("memory"),
        )