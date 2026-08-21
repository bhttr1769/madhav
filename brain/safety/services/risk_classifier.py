from brain.safety.models.action import (
    Action,
)

from brain.safety.models.risk import (
    Risk,
)


class RiskClassifier:
    """
    Classifies the potential risk of an action
    using registered classifiers.
    """

    def __init__(
        self,
        registry,
    ):

        self._registry = registry

    def classify(
        self,
        action: Action,
    ) -> Risk:

        for classifier in (
            self._registry.all()
        ):

            risk = classifier.classify(
                action,
            )

            if risk is not None:

                return risk

        raise ValueError(
            "No risk classifier matched the action."
        )