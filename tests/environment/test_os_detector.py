from brain.environment.detectors.os_detector import (
    OSDetector,
)


def test_os_detector():

    operating_system = (
        OSDetector()
    ).detect()

    assert (
        len(
            operating_system.name
        )
        > 0
    )

    assert (
        len(
            operating_system.version
        )
        > 0
    )