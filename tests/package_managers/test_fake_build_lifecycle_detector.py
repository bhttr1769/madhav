from brain.package_managers.plugins.lifecycles.fake_build_lifecycle_detector import (
    FakeBuildLifecycleDetector,
)


def test_fake_build_lifecycle_detector():

    lifecycles = (
        FakeBuildLifecycleDetector()
    ).detect(
        set(),
    )

    lifecycle = next(
        iter(
            lifecycles,
        )
    )

    assert (
        len(
            lifecycle.commands,
        )
        == 2
    )