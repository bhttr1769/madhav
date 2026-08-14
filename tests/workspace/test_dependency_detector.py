from brain.workspace.detectors.dependency_detector import (
    DependencyDetector,
)

from brain.workspace.plugins.dependencies.fake_dependency_detector import (
    FakeDependencyDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)


def test_dependency_detector():

    registry = DetectorRegistry()

    registry.register(
        FakeDependencyDetector(),
    )

    dependencies = (
        DependencyDetector(
            registry,
        )
    ).detect(
        set(),
    )

    assert len(
        dependencies
    ) == 1

    assert next(
        iter(
            dependencies,
        )
    ).name == "FakeDependency"