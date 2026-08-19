class DependencyParserRegistry:
    """
    Stores dependency parsers.
    """

    def __init__(
        self,
    ):

        self._parsers = []

    def register(
        self,
        parser,
    ):

        self._parsers.append(
            parser,
        )

    def all(
        self,
    ):

        return list(
            self._parsers,
        )

    def count(
        self,
    ):

        return len(
            self._parsers,
        )