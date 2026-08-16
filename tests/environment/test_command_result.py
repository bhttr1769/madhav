from brain.environment.models.command_result import (
    CommandResult,
)


def test_command_result():

    result = CommandResult(
        return_code=0,
        stdout="hello",
        stderr="",
    )

    assert (
        result.return_code
        == 0
    )

    assert (
        result.stdout
        == "hello"
    )

    assert (
        result.stderr
        == ""
    )