from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)


def test_engineering_decision_preserves_values():

    decision = EngineeringDecision(
        implementation_required=True,
        necessity="New implementation is required.",
        reuse_existing=False,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "The standard library provides the required functionality.",
        ),
    )

    assert decision.implementation_required is True

    assert decision.necessity == (
        "New implementation is required."
    )

    assert decision.reuse_existing is False

    assert decision.use_standard_library is True

    assert decision.use_existing_dependency is False

    assert decision.new_dependency_required is False

    assert decision.abstraction_justified is False

    assert decision.optimization_justified is False

    assert decision.rationale == (
        "The standard library provides the required functionality.",
    )


def test_engineering_decision_supports_no_new_code():

    decision = EngineeringDecision(
        implementation_required=False,
        necessity="No new code is required.",
        reuse_existing=True,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "An existing capability already satisfies the requirement.",
        ),
    )

    assert decision.implementation_required is False

    assert decision.necessity == (
        "No new code is required."
    )

    assert decision.reuse_existing is True

    assert decision.rationale == (
        "An existing capability already satisfies the requirement.",
    )


def test_engineering_decision_is_immutable():

    decision = EngineeringDecision(
        implementation_required=True,
        necessity="Implementation is required.",
        reuse_existing=False,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=True,
        optimization_justified=True,
        rationale=(
            "The abstraction is justified.",
        ),
    )

    try:
        decision.necessity = "Changed"
    except Exception:
        pass
    else:
        raise AssertionError(
            "EngineeringDecision must be immutable"
        )


def test_engineering_decision_is_dataclass():

    decision = EngineeringDecision(
        implementation_required=True,
        necessity="Implementation is required.",
        reuse_existing=False,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(),
    )

    assert decision.__dataclass_fields__