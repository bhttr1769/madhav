import pytest

from brain.environment.exceptions.unsafe_command_error import (
    UnsafeCommandError,
)

from brain.environment.models.command import (
    Command,
)

from brain.environment.validators.command_validator import (
    CommandValidator,
)


def test_safe_command():

    validator = (
        CommandValidator()
    )

    validator.validate(
        Command(
            "echo hello",
        )
    )


def test_blocked_command():

    validator = (
        CommandValidator()
    )

    with pytest.raises(
        UnsafeCommandError,
    ):

        validator.validate(
            Command(
                "shutdown now",
            )
        )