
import pytest

from brain.evolution.evolution_dependency_discovery import (
    EvolutionDependencyDiscovery,
)
from brain.package_managers.models.dependency import (
    Dependency,
)
from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


class FakePackageManagerService:
    def __init__(self, environment):
        self.environment = environment
        self.calls = []

    def analyze(self, signatures):
        self.calls.append(signatures)
        return self.environment


def create_environment():
    return PackageManagerEnvironment(
        managers=set(),
        dependency_files=set(),
        dependencies={
            Dependency(
                name="pytest",
                version="8.0.0",
                source="pyproject.toml",
            )
        },
        lifecycles=set(),
    )


def test_discovery_returns_existing_environment():
    environment = create_environment()
    service = FakePackageManagerService(
        environment
    )
    discovery = EvolutionDependencyDiscovery(
        service
    )

    signatures = frozenset()

    result = discovery.discover(
        signatures
    )

    assert result is environment
    assert service.calls == [
        signatures
    ]


def test_discovery_preserves_dependencies():
    environment = create_environment()
    discovery = EvolutionDependencyDiscovery(
        FakePackageManagerService(
            environment
        )
    )

    result = discovery.discover(
        frozenset()
    )

    assert result.dependencies == (
        environment.dependencies
    )


def test_discovery_accepts_empty_environment():
    environment = PackageManagerEnvironment(
        managers=set(),
        dependency_files=set(),
        dependencies=set(),
        lifecycles=set(),
    )

    discovery = EvolutionDependencyDiscovery(
        FakePackageManagerService(
            environment
        )
    )

    result = discovery.discover(
        frozenset()
    )

    assert result is environment
    assert result.dependencies == set()


def test_discovery_rejects_missing_signatures():
    service = FakePackageManagerService(
        create_environment()
    )
    discovery = EvolutionDependencyDiscovery(
        service
    )

    with pytest.raises(
        TypeError,
        match="signatures must not be None",
    ):
        discovery.discover(
            None
        )

    assert service.calls == []


def test_discovery_rejects_invalid_service():
    with pytest.raises(
        TypeError,
        match="must expose a callable analyze",
    ):
        EvolutionDependencyDiscovery(
            object()
        )


def test_discovery_rejects_invalid_result():
    discovery = EvolutionDependencyDiscovery(
        FakePackageManagerService(
            {"dependencies": set()}
        )
    )

    with pytest.raises(
        TypeError,
        match="must return a PackageManagerEnvironment",
    ):
        discovery.discover(
            frozenset()
        )


def test_discovery_propagates_service_failure():
    class FailingService:
        def analyze(self, signatures):
            raise RuntimeError(
                "dependency analysis failed"
            )

    discovery = EvolutionDependencyDiscovery(
        FailingService()
    )

    with pytest.raises(
        RuntimeError,
        match="dependency analysis failed",
    ):
        discovery.discover(
            frozenset()
        )