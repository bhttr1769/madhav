class RiskClassifierRegistry:
    """
    Stores risk classifiers.
    """

    def __init__(
        self,
    ):

        self._classifiers = []

    def register(
        self,
        classifier,
    ):

        self._classifiers.append(
            classifier,
        )

    def all(
        self,
    ):

        return list(
            self._classifiers,
        )

    def count(
        self,
    ):

        return len(
            self._classifiers,
        )