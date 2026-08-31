from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


def test_generation_result_preserves_values():

    change = CodeChange(
        path="brain/example.py",
        operation="create",
        content="print('hello')",
    )

    decision = EngineeringDecision(
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

    result = GenerationResult(
        changes=(change,),
        decision=decision,
    )

    assert result.changes == (change,)

    assert result.decision == decision


def test_generation_result_supports_no_code_changes():

    decision = EngineeringDecision(
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

    result = GenerationResult(
        changes=(),
        decision=decision,
    )

    assert result.changes == ()

    assert result.decision == decision


def test_generation_result_is_immutable():

    decision = EngineeringDecision(
        necessity="Implementation is required.",
        reuse_existing=False,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(),
    )

    result = GenerationResult(
        changes=(),
        decision=decision,
    )

    try:
        result.changes = ()
    except Exception:
        pass
    else:
        raise AssertionError(
            "GenerationResult must be immutable"
        )


def test_generation_result_is_dataclass():

    decision = EngineeringDecision(
        necessity="Implementation is required.",
        reuse_existing=False,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(),
    )

    result = GenerationResult(
        changes=(),
        decision=decision,
    )

    assert result.__dataclass_fields__