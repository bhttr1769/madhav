from typing import Protocol

from brain.agents.context_source import ContextSource
from brain.agents.models.context_source_result import ContextSourceResult


class ContextSourceProvider(Protocol):
    source: ContextSource

    def provide(self) -> ContextSourceResult:
        ...