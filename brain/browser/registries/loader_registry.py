class LoaderRegistry:
    """
    Stores document loaders.
    """

    def __init__(
        self,
    ):

        self._loaders = []

    def register(
        self,
        loader,
    ) -> None:

        self._loaders.append(
            loader,
        )

    def all(
        self,
    ):

        return list(
            self._loaders,
        )