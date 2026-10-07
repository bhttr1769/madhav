from brain.agents.context_source import ContextSource
from brain.agents.context_source_provider import ContextSourceProvider
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.context_source_result import ContextSourceResult


class ContextSourceCoordinator:
    """
    Coordinates existing context source providers.

    This class does not create, retrieve, transform, or persist
    source data. It only requests source values and records their
    availability.
    """

    def coordinate(
        self,
        providers: tuple[ContextSourceProvider, ...],
        requested_sources: frozenset[ContextSource],
    ) -> dict[ContextSource, ContextSourceResult]:

        if not isinstance(requested_sources, frozenset):
            raise TypeError(
                "requested_sources must be a frozenset"
            )

        for source in requested_sources:
            if not isinstance(source, ContextSource):
                raise TypeError(
                    "requested_sources must contain only ContextSource values"
                )

        results: dict[ContextSource, ContextSourceResult] = {}

        provider_map = {
            provider.source: provider
            for provider in providers
        }

        for source in ContextSource:
            if source not in requested_sources:
                results[source] = ContextSourceResult(
                    source=source,
                    status=ContextSourceStatus.NOT_REQUESTED,
                )
                continue

            provider = provider_map.get(source)

            if provider is None:
                results[source] = ContextSourceResult(
                    source=source,
                    status=ContextSourceStatus.UNAVAILABLE,
                )
                continue

            try:
                result = provider.provide()
            except Exception as exc:
                results[source] = ContextSourceResult(
                    source=source,
                    status=ContextSourceStatus.FAILED,
                    error=exc,
                )
                continue

            if not isinstance(result, ContextSourceResult):
                raise TypeError(
                    "provider must return ContextSourceResult"
                )

            results[source] = result

        return results