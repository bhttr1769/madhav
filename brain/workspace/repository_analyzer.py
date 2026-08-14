from pathlib import Path


class RepositoryAnalyzer:
    """
    Identifies important repository files.
    """

    IMPORTANT_FILES = {
        "pom.xml": "Maven",
        "package.json": "Node.js",
        "requirements.txt": "Python",
        "README.md": "Documentation",
        "Dockerfile": "Docker",
    }

    def analyze(
        self,
        files: list[Path],
    ) -> set[str]:

        detected = set()

        for file in files:

            technology = self.IMPORTANT_FILES.get(
                file.name
            )

            if technology:

                detected.add(
                    technology
                )

        return detected