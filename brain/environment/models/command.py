from dataclasses import dataclass

from brain.safety.models.action import (
    Action,
)


@dataclass(
    frozen=True,
)
class Command:
    """
    Represents a terminal command.
    """

    value: str

    def to_action(
        self,
    ) -> Action:

        return Action(
            name="execute",
            category="command",
            target=self.value,
        )