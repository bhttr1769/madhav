from brain.evolution.models.evolution_discovery_request import (
    EvolutionDiscoveryRequest,
)


def test_evolution_discovery_request_stores_provider():
    provider = object()

    request = EvolutionDiscoveryRequest(
        provider=provider,
    )

    assert request.provider is provider