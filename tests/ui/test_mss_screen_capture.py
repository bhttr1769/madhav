from pathlib import Path

from brain.ui.capture.mss_screen_capture import (
    MSSScreenCapture,
)

from brain.ui.models.screen import (
    Screen,
)


def test_mss_screen_capture_returns_screen(
    tmp_path: Path,
):

    capture = MSSScreenCapture(
        output_directory=tmp_path,
    )

    result = capture.capture()

    assert isinstance(
        result,
        Screen,
    )

    assert result.width > 0
    assert result.height > 0


def test_mss_screen_capture_creates_image(
    tmp_path: Path,
):

    capture = MSSScreenCapture(
        output_directory=tmp_path,
    )

    result = capture.capture()

    assert result.image_path is not None

    image_path = Path(
        result.image_path,
    )

    assert image_path.exists()
    assert image_path.is_file()
    assert image_path.suffix == ".png"
    assert image_path.stat().st_size > 0


def test_mss_screen_capture_uses_configured_directory(
    tmp_path: Path,
):

    output_directory = (
        tmp_path / "screens"
    )

    capture = MSSScreenCapture(
        output_directory=output_directory,
    )

    result = capture.capture()

    assert result.image_path is not None

    image_path = Path(
        result.image_path,
    )

    assert image_path.parent == (
        output_directory
    )


def test_mss_screen_capture_creates_unique_files(
    tmp_path: Path,
):

    capture = MSSScreenCapture(
        output_directory=tmp_path,
    )

    first = capture.capture()
    second = capture.capture()

    assert first.image_path != second.image_path

    assert Path(
        first.image_path,
    ).exists()

    assert Path(
        second.image_path,
    ).exists()