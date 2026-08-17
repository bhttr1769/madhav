from abc import ABC
from abc import abstractmethod

from brain.environment.models.command import (
    Command,
)

from brain.environment.models.command_result import (
    CommandResult,
)


class BaseTerminal(
    ABC,
):

    @abstractmethod
    def execute(
        self,
        command: Command,
    ) -> CommandResult:

        pass