from brain.browser.loaders.html_loader import (
    HtmlLoader,
)

from brain.browser.registries.loader_registry import (
    LoaderRegistry,
)


def test_loader_registry():

    registry = (
        LoaderRegistry()
    )

    registry.register(
        HtmlLoader(),
    )

    assert (
        len(
            registry.all()
        )
        == 1
    )