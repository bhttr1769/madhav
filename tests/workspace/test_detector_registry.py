from brain.workspace.detectors.base_detector import (
    BaseDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)


class FakeDetector(
    BaseDetector,
):

    def detect(
        self,
        signatures,
    ):

        return None


def test_detector_registry():

    registry = DetectorRegistry()

    detector = FakeDetector()

    registry.register(
        detector,
    )

    assert (
        registry.count()
        == 1
    )

    assert (
        detector
        in registry.all()
    )