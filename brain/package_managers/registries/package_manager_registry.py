class PackageManagerRegistry:
    """
    Stores package-manager plugins.
    """

    def __init__(
        self,
    ):

        self._plugins = []

    def register(
        self,
        plugin,
    ):

        self._plugins.append(
            plugin,
        )

    def all(
        self,
    ):

        return list(
            self._plugins,
        )

    def count(
        self,
    ):

        return len(
            self._plugins,
        )