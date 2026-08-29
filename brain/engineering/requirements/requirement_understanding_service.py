from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.requirements.requirement_interpreter import (
    RequirementInterpreter,
)


class RequirementUnderstandingService:
    """
    Converts a raw engineering request into
    structured requirement understanding.
    """

    def __init__(
        self,
        interpreter: RequirementInterpreter,
    ):
        if not isinstance(
            interpreter,
            RequirementInterpreter,
        ):
            raise TypeError(
                "interpreter must be a RequirementInterpreter"
            )

        self._interpreter = interpreter

    def understand(
        self,
        request: str,
    ) -> Requirement:

        if not isinstance(request, str):
            raise TypeError(
                "request must be a string"
            )

        request = request.strip()

        if not request:
            raise ValueError(
                "request must not be empty"
            )

        requirement = self._interpreter.interpret(
            request,
        )

        if not isinstance(
            requirement,
            Requirement,
        ):
            raise TypeError(
                "interpreter must return a Requirement"
            )

        return requirement