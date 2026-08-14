from brain.workspace.detectors.build_system_detector import (
    BuildSystemDetector,
)

from brain.workspace.plugins.build_systems.fake_build_system_detector import (
    FakeBuildSystemDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)


def test_build_system_detector():

    registry = DetectorRegistry()

    registry.register(
        FakeBuildSystemDetector(),
    )

    technologies = (
        BuildSystemDetector(
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
    ).name == "FakeBuildSystem"