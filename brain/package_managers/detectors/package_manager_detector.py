class PackageManagerDetector:
    """
    Executes registered package-manager plugins.
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

        managers = set()

        for plugin in self._registry.all():

            managers.update(
                plugin.detect(
                    signatures,
                )
            )

        return managers