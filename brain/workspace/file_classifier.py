from pathlib import Path


class FileClassifier:
    """
    Classifies project files.
    """

    def classify(
        self,
        file: Path,
    ) -> str:

        suffix = file.suffix.lower()

        if file.name.startswith(
            "test_"
        ):

            return "test"

        if suffix in {
            ".py",
            ".java",
            ".js",
        }:

            return "source"

        if suffix == ".md":

            return "documentation"

        if suffix in {
            ".json",
            ".yaml",
            ".yml",
        }:

            return "configuration"

        return "other"