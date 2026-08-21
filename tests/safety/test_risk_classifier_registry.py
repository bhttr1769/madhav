from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)


class FakeRiskClassifier:

    def classify(
        self,
        action,
    ):

        pass


def test_risk_classifier_registry():

    registry = (
        RiskClassifierRegistry()
    )

    classifier = (
        FakeRiskClassifier()
    )

    registry.register(
        classifier,
    )

    assert (
        registry.count()
        == 1
    )

    assert (
        len(
            registry.all(),
        )
        == 1
    )

    assert (
        registry.all()[0]
        == classifier
    )