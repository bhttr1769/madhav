class BrowserEngine:

    def __init__(
        self,
        client,
        loader_registry,
        parser_registry,
        extractor_registry,
        cleaner_registry,
    ):

        self._client = client

        self._loader_registry = (
            loader_registry
        )

        self._parser_registry = (
            parser_registry
        )

        self._extractor_registry = (
            extractor_registry
        )

        self._cleaner_registry = (
            cleaner_registry
        )

    def learn(
        self,
        url,
    ):

        response = (
            self._client.get(
                url,
            )
        )

        loader = next(
            loader
            for loader
            in self._loader_registry.all()
            if loader.can_load(
                response,
            )
        )

        content = loader.load(
            response,
        )

        parser = next(
            parser
            for parser
            in self._parser_registry.all()
            if parser.can_parse(
                content,
            )
        )

        document = parser.parse(
            content,
        )

        extractor = next(
            extractor
            for extractor
            in self._extractor_registry.all()
            if extractor.can_extract(
                document,
            )
        )

        extracted = (
            extractor.extract(
                document,
            )
        )

        cleaner = next(
            cleaner
            for cleaner
            in self._cleaner_registry.all()
            if cleaner.can_clean(
                extracted,
            )
        )

        return cleaner.clean(
            extracted,
        )