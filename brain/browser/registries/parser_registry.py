class ParserRegistry:
    """
    Stores document parsers.
    """

    def __init__(
        self,
    ):

        self._parsers = []

    def register(
        self,
        parser,
    ) -> None:

        self._parsers.append(
            parser,
        )

    def all(
        self,
    ):

        return list(
            self._parsers,
        )