from pathlib import Path


class RecursiveDirectoryScanner:
    """
    Recursively scans directories.
    """

    def scan(
        self,
        directory: str | Path,
    ) -> list[Path]:

        directory = Path(directory)

        return [
            path
            for path in directory.rglob("*")
            if path.is_file()
        ]