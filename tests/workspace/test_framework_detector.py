from brain.workspace.detectors.framework_detector import (
    FrameworkDetector,
)

from brain.workspace.plugins.frameworks.fake_framework_detector import (
    FakeFrameworkDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)


def test_framework_detector():

    registry = DetectorRegistry()

    registry.register(
        FakeFrameworkDetector(),
    )

    technologies = (
        FrameworkDetector(
            registry,
        )
    ).detect(
        set(),
    )

    assert len(
        technologies
    ) == 1

    assert next(
        iter(
            technologies,
        )
    ).name == "FakeFramework"