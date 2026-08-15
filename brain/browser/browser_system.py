class BrowserSystem:

    def __init__(
        self,
        memory_learner,
        graph_learner,
    ):

        self._memory_learner = (
            memory_learner
        )

        self._graph_learner = (
            graph_learner
        )

    def learn(
        self,
        url,
    ):

        content = (
            self._memory_learner.learn(
                url,
            )
        )

        self._graph_learner.learn(
            url,
        )

        return content