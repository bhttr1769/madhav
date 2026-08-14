from pathlib import Path
from datetime import datetime


class FileWatcher:
    """
    Tracks file modifications.
    """

    def modified_at(
        self,
        file_path: str | Path,
    ) -> datetime:

        file_path = Path(file_path)

        return datetime.fromtimestamp(
            file_path.stat().st_mtime
        )