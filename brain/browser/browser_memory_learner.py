class BrowserMemoryLearner:

    def __init__(
        self,
        browser_engine,
        memory,
    ):

        self._browser_engine = (
            browser_engine
        )

        self._memory = memory

    def learn(
        self,
        url,
    ):

        content = (
            self._browser_engine.learn(
                url,
            )
        )

        self._memory.add(
            content.text,
        )

        return content