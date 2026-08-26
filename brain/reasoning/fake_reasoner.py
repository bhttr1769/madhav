from brain.reasoning.models.context import (
    Context,
)

from brain.reasoning.reasoner import (
    Reasoner,
)


class FakeReasoner(Reasoner):
    """
    Deterministic reasoner for testing.
    """

    def __init__(
        self,
        result,
    ):
        self._result = result

    def reason(
        self,
        context: Context,
    ):
        return self._result