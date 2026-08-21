from brain.safety.models.action import (
    Action,
)

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)

from brain.safety.services.risk_classifier import (
    RiskClassifier,
)


class FakeRiskClassifier:

    def classify(
        self,
        action,
    ):

        return Risk.HIGH


def test_risk_classifier():

    registry = (
        RiskClassifierRegistry()
    )

    registry.register(
        FakeRiskClassifier(),
    )

    classifier = RiskClassifier(
        registry,
    )

    risk = classifier.classify(
        Action(
            name="execute",
            category="command",
            target="test",
        ),
    )

    assert (
        risk
        == Risk.HIGH
    )


def test_risk_classifier_without_match():

    registry = (
        RiskClassifierRegistry()
    )

    classifier = RiskClassifier(
        registry,
    )

    try:

        classifier.classify(
            Action(
                name="execute",
                category="command",
                target="test",
            ),
        )

    except ValueError as error:

        assert (
            str(error)
            == "No risk classifier matched the action."
        )

    else:

        raise AssertionError(
            "Expected ValueError."
        )