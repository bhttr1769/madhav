from brain.package_managers.detectors.build_lifecycle_detector import (
    BuildLifecycleDetector,
)

from brain.package_managers.plugins.lifecycles.fake_build_lifecycle_detector import (
    FakeBuildLifecycleDetector,
)

from brain.package_managers.registries.build_lifecycle_registry import (
    BuildLifecycleRegistry,
)


def test_build_lifecycle_detector():

    registry = (
        BuildLifecycleRegistry()
    )

    registry.register(
        FakeBuildLifecycleDetector(),
    )

    lifecycles = (
        BuildLifecycleDetector(
            registry,
        )
    ).detect(
        set(),
    )

    assert (
        len(
            lifecycles,
        )
        == 1
    )