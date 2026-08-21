class PolicyRegistry:
    """
    Stores safety policies.
    """

    def __init__(
        self,
    ):

        self._policies = []

    def register(
        self,
        policy,
    ):

        self._policies.append(
            policy,
        )

    def all(
        self,
    ):

        return list(
            self._policies,
        )

    def find(
        self,
        category,
    ):

        for policy in self._policies:

            if (
                policy.category
                == category
            ):

                return policy

        return None

    def count(
        self,
    ):

        return len(
            self._policies,
        )