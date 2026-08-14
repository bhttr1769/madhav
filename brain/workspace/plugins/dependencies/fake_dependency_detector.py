from brain.workspace.detectors.base_detector import (
    BaseDetector,
)

from brain.workspace.models.dependency import (
    Dependency,
)


class FakeDependencyDetector(
    BaseDetector,
):

    def detect(
        self,
        signatures,
    ):

        return {
            Dependency(
                name="FakeDependency",
            )
        }