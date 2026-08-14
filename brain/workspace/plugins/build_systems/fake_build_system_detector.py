from brain.workspace.detectors.base_detector import (
    BaseDetector,
)

from brain.workspace.models.technology import (
    Technology,
)


class FakeBuildSystemDetector(
    BaseDetector,
):

    def detect(
        self,
        signatures,
    ):

        return {
            Technology(
                name="FakeBuildSystem",
                category="build_system",
            )
        }