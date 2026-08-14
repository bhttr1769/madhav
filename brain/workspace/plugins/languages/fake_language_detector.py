from brain.workspace.detectors.base_detector import (
    BaseDetector,
)

from brain.workspace.models.technology import (
    Technology,
)


class FakeLanguageDetector(
    BaseDetector,
):

    def detect(
        self,
        signatures,
    ):

        return {
            Technology(
                name="FakeLanguage",
                category="language",
            )
        }