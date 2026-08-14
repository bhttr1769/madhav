import time

from brain.filesystem.change_detector import (
    ChangeDetector,
)


def test_change_detector(
    tmp_path,
):

    file = tmp_path / "notes.txt"

    file.write_text(
        "version 1"
    )

    detector = ChangeDetector()

    assert detector.changed(
        file,
    )

    assert not detector.changed(
        file,
    )

    time.sleep(1)

    file.write_text(
        "version 2"
    )

    assert detector.changed(
        file,
    )