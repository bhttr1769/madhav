from brain.workspace.detectors.base_detector import (
    BaseDetector,
)


class DetectorRegistry:
    """
    Stores and manages workspace detectors.
    """

    def __init__(self):

        self._detectors: list[
            BaseDetector
        ] = []

    def register(
        self,
        detector: BaseDetector,
    ) -> None:

        self._detectors.append(
            detector,
        )

    def all(
        self,
    ) -> list[BaseDetector]:

        return list(
            self._detectors
        )

    def count(
        self,
    ) -> int:

        return len(
            self._detectors
        )