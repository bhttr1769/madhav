class DependencyDetector:
    """
    Executes registered dependency parsers.
    """

    def __init__(
        self,
        registry,
    ):

        self._registry = registry

    def detect(
        self,
        dependency_files,
    ):

        dependencies = set()

        for parser in self._registry.all():

            for dependency_file in dependency_files:

                dependencies.update(
                    parser.parse(
                        dependency_file,
                    )
                )

        return dependencies