from pathlib import Path


class FileClassifier:
    """
    Classifies repository files.
    """

    TEST_DIRECTORIES = {
        "test",
        "tests",
        "__tests__",
    }

    DOCUMENTATION_NAMES = {
        "readme",
        "changelog",
        "contributing",
        "license",
    }

    CONFIGURATION_NAMES = {
        ".gitignore",
        ".env",
        ".editorconfig",
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "pom.xml",
        "build.gradle",
        "settings.gradle",
        "cargo.toml",
        "go.mod",
    }

    def classify(
        self,
        path: Path,
    ) -> str:

        name = path.name.lower()

        parts = {
            part.lower()
            for part in path.parts
        }

        if (
            name in self.CONFIGURATION_NAMES
            or name.endswith(".config")
        ):
            return "configuration"

        if (
            "test" in parts
            or "tests" in parts
            or "__tests__" in parts
            or name.startswith("test_")
            or name.endswith("_test.py")
            or name.endswith(".test.js")
            or name.endswith(".test.ts")
        ):
            return "test"

        stem = path.stem.lower()

        if (
            stem in self.DOCUMENTATION_NAMES
            or path.suffix.lower()
            in {
                ".md",
                ".rst",
                ".txt",
            }
        ):
            return "documentation"

        if path.suffix:
            return "source"

        return "other"