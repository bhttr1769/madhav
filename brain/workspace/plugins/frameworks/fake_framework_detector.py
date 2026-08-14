from brain.workspace.detectors.base_detector import (
    BaseDetector,
)

from brain.workspace.models.technology import (
    Technology,
)


class FakeFrameworkDetector(
    BaseDetector,
):

    def detect(
        self,
        signatures,
    ):

        return {
            Technology(
                name="FakeFramework",
                category="framework",
            )
        }