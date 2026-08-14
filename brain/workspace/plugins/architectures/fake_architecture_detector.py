from brain.workspace.detectors.base_detector import (
    BaseDetector,
)

from brain.workspace.models.architecture import (
    Architecture,
)


class FakeArchitectureDetector(
    BaseDetector,
):

    def detect(
        self,
        signatures,
    ):

        return {
            Architecture(
                name="FakeArchitecture",
            )
        }