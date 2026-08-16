from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class CommandResult:
    """
    Represents a command execution result.
    """

    return_code: int

    stdout: str

    stderr: str