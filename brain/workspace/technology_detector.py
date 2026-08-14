from pathlib import Path


class TechnologyDetector:
    """
    Detects technologies used in a project.
    """

    EXTENSIONS = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".json": "JSON",
        ".md": "Markdown",
    }

    def detect(
        self,
        files: list[Path],
    ) -> set[str]:

        technologies = set()

        for file in files:

            technology = self.EXTENSIONS.get(
                file.suffix.lower()
            )

            if technology:

                technologies.add(
                    technology
                )

        return technologies