from pathlib import Path


class FileFilter:
    """
    Filters files by extension.
    """

    def by_extension(
        self,
        files: list[Path],
        extension: str,
    ) -> list[Path]:

        extension = extension.lower()

        return [
            file
            for file in files
            if file.suffix.lower() == extension
        ]