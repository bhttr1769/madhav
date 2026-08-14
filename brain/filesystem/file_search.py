from pathlib import Path


class FileSearch:
    """
    Searches files by name.
    """

    def by_name(
        self,
        files: list[Path],
        query: str,
    ) -> list[Path]:

        query = query.lower()

        return [
            file
            for file in files
            if query in file.name.lower()
        ]