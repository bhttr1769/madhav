from pathlib import Path


class SupportedFileFilter:
    """
    Filters files supported by Madhav.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".pdf",
        ".docx",
    }

    def filter(
        self,
        files: list[Path],
    ) -> list[Path]:

        return [
            file
            for file in files
            if file.suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        ]