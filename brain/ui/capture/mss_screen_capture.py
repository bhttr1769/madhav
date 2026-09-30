from datetime import datetime
from pathlib import Path

from mss import MSS
from mss.tools import to_png

from brain.ui.capture.screen_capture import (
    ScreenCapture,
)

from brain.ui.models.screen import (
    Screen,
)


class MSSScreenCapture(ScreenCapture):
    """
    Real screen-capture implementation using MSS.
    """

    def __init__(
        self,
        output_directory: str | Path,
    ):
        self._output_directory = Path(
            output_directory
        )

    def capture(self) -> Screen:
        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        image_path = (
            self._output_directory
            / f"screen_{timestamp}.png"
        )

        with MSS() as capture:
            monitor = capture.primary_monitor

            screenshot = capture.grab(
                monitor,
            )

            to_png(
                screenshot.rgb,
                screenshot.size,
                output=str(image_path),
            )

        return Screen(
            width=monitor["width"],
            height=monitor["height"],
            image_path=str(image_path),
        )