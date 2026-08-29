from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.requirements.requirement_interpreter import (
    RequirementInterpreter,
)


class FakeRequirementInterpreter(
    RequirementInterpreter,
):
    """
    Deterministic requirement interpreter for testing.
    """

    def __init__(
        self,
        result: Requirement,
    ):
        self._result = result

    def interpret(
        self,
        request: str,
    ) -> Requirement:

        return self._result