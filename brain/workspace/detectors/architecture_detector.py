class ArchitectureDetector:
    """
    Executes registered architecture plugins.
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

        architectures = set()

        for detector in self._registry.all():

            architectures.update(
                detector.detect(
                    signatures,
                )
            )

        return architectures