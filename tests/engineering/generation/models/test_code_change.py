from brain.engineering.generation.models.code_change import (
    CodeChange,
)


def test_code_change_preserves_values():

    change = CodeChange(
        path="brain/example.py",
        operation="create",
        content="print('hello')",
    )

    assert change.path == "brain/example.py"
    assert change.operation == "create"
    assert change.content == "print('hello')"


def test_code_change_is_immutable():

    change = CodeChange(
        path="brain/example.py",
        operation="create",
        content="print('hello')",
    )

    try:
        change.path = "other.py"
    except Exception:
        pass
    else:
        raise AssertionError(
            "CodeChange must be immutable"
        )


def test_code_change_is_dataclass():

    change = CodeChange(
        path="brain/example.py",
        operation="modify",
        content="updated",
    )

    assert change.__dataclass_fields__