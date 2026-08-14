class DependencyDetector:
    """
    Executes registered dependency plugins.
    """

    def __init__(
        self,
        registry,
    ):

        self._registry = registry

    def detect(
        self,
        signatures,
    ):

        dependencies = set()

        for detector in self._registry.all():

            dependencies.update(
                detector.detect(
                    signatures,
                )
            )

        return dependencies