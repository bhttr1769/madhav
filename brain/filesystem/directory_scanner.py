from pathlib import Path


class DirectoryScanner:
    """
    Scans directories for files.
    """

    def scan(
        self,
        directory: str | Path,
    ) -> list[Path]:

        directory = Path(directory)

        return [
            file
            for file in directory.iterdir()
            if file.is_file()
        ]