from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionDiscoveryRequest:
    provider: object
    repository_path: str