class CleanerRegistry:
    """
    Stores content cleaners.
    """

    def __init__(
        self,
    ):

        self._cleaners = []

    def register(
        self,
        cleaner,
    ) -> None:

        self._cleaners.append(
            cleaner,
        )

    def all(
        self,
    ):

        return list(
            self._cleaners,
        )