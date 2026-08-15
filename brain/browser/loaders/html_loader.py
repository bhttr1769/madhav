from brain.browser.loaders.base_loader import (
    BaseLoader,
)


class HtmlLoader(
    BaseLoader,
):

    def can_load(
        self,
        response,
    ) -> bool:

        return (
            "<html"
            in response.content.lower()
        )

    def load(
        self,
        response,
    ):

        return response.content