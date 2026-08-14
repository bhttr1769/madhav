from brain.workspace.models.technology import (
    Technology,
)


class FrameworkDetector:
    """
    Executes registered framework plugins.
    """

    def __init__(
        self,
        registry,
    ):

        self._registry = registry

    def detect(
        self,
        signatures,
    ) -> set[Technology]:

        technologies = set()

        for detector in self._registry.all():

            technologies.update(
                detector.detect(
                    signatures,
                )
            )

        return technologies