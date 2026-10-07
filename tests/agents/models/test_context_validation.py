from brain.agents.models.context_validation import ContextValidation


def test_valid_context_validation():
    result = ContextValidation(
        valid=True,
        errors=(),
    )

    assert result.valid is True
    assert result.errors == ()


def test_invalid_context_validation():
    result = ContextValidation(
        valid=False,
        errors=("runtime_id must not be empty",),
    )

    assert result.valid is False
    assert result.errors == (
        "runtime_id must not be empty",
    )


def test_validation_is_immutable():
    result = ContextValidation(
        valid=True,
        errors=(),
    )

    try:
        result.valid = False
        assert False
    except AttributeError:
        pass