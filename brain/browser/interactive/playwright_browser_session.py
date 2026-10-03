from pathlib import Path

from playwright.sync_api import sync_playwright

from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.models.browser_session_state import (
    BrowserSessionState,
)

from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)

from brain.browser.url_validator import UrlValidator

from brain.browser.interactive.models.browser_element import (
    BrowserElement,
)

class PlaywrightBrowserSession(BrowserSession):

    def __init__(
        self,
        executable_path: str,
        url_validator: UrlValidator | None = None,
    ):
        if not isinstance(executable_path, str):
            raise TypeError("executable_path must be a string")

        if not executable_path.strip():
            raise ValueError("executable_path must not be empty")

        if not Path(executable_path).is_file():
            raise ValueError(
                "executable_path must point to an existing file"
            )

        self._executable_path = executable_path
        self._playwright = None
        self._browser = None
        self._page = None
        self._url_validator = (
            url_validator
            if url_validator is not None
            else UrlValidator()
        )

    def start(self) -> None:
        if self._browser is not None:
            raise RuntimeError("browser session is already active")

        self._playwright = sync_playwright().start()

        try:
            self._browser = self._playwright.chromium.launch(
                executable_path=self._executable_path
            )
            self._page = self._browser.new_page()
        except Exception:
            self._cleanup()
            raise

    def close(self) -> None:
        if self._browser is None:
            return

        try:
            self._browser.close()
        finally:
            self._cleanup()

    def navigate(self, url: str) -> None:
        if not isinstance(url, str):
            raise TypeError("url must be a string")

        if not url.strip():
            raise ValueError("url must not be empty")

        if self._page is None:
            raise RuntimeError("browser session is not active")

        normalized_url = self._url_validator.normalize(url)

        if not self._url_validator.is_valid(normalized_url):
            raise ValueError("invalid URL")

        self._page.goto(normalized_url)

    def current_state(self) -> BrowserSessionState:
        if self._page is None:
            return BrowserSessionState(
                active=False,
                url=None,
            )

        return BrowserSessionState(
            active=True,
            url=self._page.url,
        )

    def _cleanup(self) -> None:
        self._page = None
        self._browser = None

        if self._playwright is not None:
            self._playwright.stop()

        self._playwright = None

    def observe(self) -> BrowserObservation:
        if self._page is None:
            raise RuntimeError("browser session is not active")

        elements = self._observe_elements()

        return BrowserObservation(
            url=self._page.url,
            title=self._page.title(),
            text=self._page.locator("body").inner_text(),
            elements=elements,
        )

    def _observe_elements(self) -> frozenset[BrowserElement]:
        locator = self._page.locator(
            "a, button, input, textarea, select, "
            "[role='button'], [role='link'], [role='textbox']"
        )

        elements = set()

        for index in range(locator.count()):
            element = locator.nth(index)

            data = element.evaluate(
                """
                element => {
                    const tag = element.tagName.toLowerCase();

                    const role = element.getAttribute("role");

                    let elementType = tag;

                    if (role) {
                        elementType = role;
                    }

                    const name =
                        element.getAttribute("aria-label") ||
                        element.getAttribute("name") ||
                        element.getAttribute("title") ||
                        null;

                    const text =
                        element.innerText ||
                        element.textContent ||
                        null;

                    const selectorParts = [];
                    let current = element;
 
                    while (
                        current &&
                        current.nodeType === Node.ELEMENT_NODE
                    ) {
                        let selector = current.tagName.toLowerCase();

                        if (current.id) {
                            selector += "#" + CSS.escape(current.id);
                            selectorParts.unshift(selector);
                            break;
                        }

                        let sibling = current;
                        let index = 1;
 
                        while (
                            sibling.previousElementSibling
                        ) {
                            sibling = sibling.previousElementSibling;

                            if (
                                sibling.tagName === current.tagName
                            ) {
                                index += 1;
                            }
                        }

                        selector += `:nth-of-type(${index})`;
 
                        selectorParts.unshift(selector);
                        current = current.parentElement;
                    }

                    return {
                        element_type: elementType,
                        name: name,
                        text: text ? text.trim() : null,
                        selector: selectorParts.join(">"),
                        interactive: true,
                    };
                }
                """
            )

            elements.add(
                BrowserElement(
                    element_type=data["element_type"],
                    name=data["name"],
                    text=data["text"],
                    selector=data["selector"],
                    interactive=data["interactive"],
                )
            )

        return frozenset(elements)  