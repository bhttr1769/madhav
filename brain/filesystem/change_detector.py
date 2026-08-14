from pathlib import Path

from brain.filesystem.file_watcher import (
    FileWatcher,
)


class ChangeDetector:
    """
    Detects whether a file has changed.
    """

    def __init__(self):

        self._watcher = FileWatcher()

        self._timestamps = {}

    def changed(
        self,
        file_path: str | Path,
    ) -> bool:

        file_path = Path(file_path)

        current = self._watcher.modified_at(
            file_path,
        )

        previous = self._timestamps.get(
            str(file_path),
        )

        self._timestamps[
            str(file_path)
        ] = current

        if previous is None:

            return True

        return current > previous