class ExtractorRegistry:
    """
    Stores content extractors.
    """

    def __init__(
        self,
    ):

        self._extractors = []

    def register(
        self,
        extractor,
    ) -> None:

        self._extractors.append(
            extractor,
        )

    def all(
        self,
    ):

        return list(
            self._extractors,
        )