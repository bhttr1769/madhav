from dataclasses import dataclass


@dataclass(frozen=True)
class BrowserSessionState:
    active: bool
    url: str | None