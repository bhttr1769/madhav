from brain.package_managers.plugins.lifecycles.fake_build_lifecycle_detector import (
    FakeBuildLifecycleDetector,
)

from brain.package_managers.registries.build_lifecycle_registry import (
    BuildLifecycleRegistry,
)


def test_build_lifecycle_registry():

    registry = (
        BuildLifecycleRegistry()
    )

    registry.register(
        FakeBuildLifecycleDetector(),
    )

    assert (
        registry.count()
        == 1
    )

    assert (
        len(
            registry.all(),
        )
        == 1
    )