from brain.package_managers.models.dependency_file import (
    DependencyFile,
)


class DependencyFileDetector:
    """
    Executes registered dependency-file plugins.
    """

    def __init__(
        self,
        registry,
    ):

        self._registry = registry

    def detect(
        self,
        signatures,
    ) -> set[DependencyFile]:

        files = set()

        for plugin in self._registry.all():

            files.update(
                plugin.detect(
                    signatures,
                )
            )

        return files