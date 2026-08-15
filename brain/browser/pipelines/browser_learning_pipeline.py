from brain.browser.cleaners.text_cleaner import (
    TextCleaner,
)

from brain.browser.clients.http_client import (
    HttpClient,
)

from brain.browser.extractors.html_extractor import (
    HtmlExtractor,
)

from brain.browser.loaders.html_loader import (
    HtmlLoader,
)

from brain.browser.parsers.html_parser import (
    HtmlParser,
)

from brain.browser.url_validator import (
    UrlValidator,
)


class BrowserLearningPipeline:
    """
    Browser learning pipeline.
    """

    def __init__(self):

        self._validator = (
            UrlValidator()
        )

        self._client = (
            HttpClient()
        )

        self._loader = (
            HtmlLoader()
        )

        self._parser = (
            HtmlParser()
        )

        self._extractor = (
            HtmlExtractor()
        )

        self._cleaner = (
            TextCleaner()
        )

    def learn(
        self,
        url: str,
    ):

        url = self._validator.normalize(
            url,
        )

        response = self._client.get(
            url,
        )

        loaded = self._loader.load(
            response,
        )

        document = self._parser.parse(
            loaded,
        )

        extracted = (
            self._extractor.extract(
                document,
            )
        )

        return self._cleaner.clean(
            extracted,
        )