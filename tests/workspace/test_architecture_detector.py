from brain.workspace.detectors.architecture_detector import (
    ArchitectureDetector,
)

from brain.workspace.plugins.architectures.fake_architecture_detector import (
    FakeArchitectureDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)


def test_architecture_detector():

    registry = DetectorRegistry()

    registry.register(
        FakeArchitectureDetector(),
    )

    architectures = (
        ArchitectureDetector(
            registry,
        )
    ).detect(
        set(),
    )

    assert len(
        architectures
    ) == 1

    assert next(
        iter(
            architectures,
        )
    ).name == "FakeArchitecture"