from pathlib import Path


class DirectoryNavigator:
    """
    Provides directory navigation utilities.
    """

    def directories(
        self,
        directory: str | Path,
    ) -> list[Path]:

        directory = Path(directory)

        return [
            path
            for path in directory.iterdir()
            if path.is_dir()
        ]