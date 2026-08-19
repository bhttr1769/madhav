from brain.package_managers.models.package_manager import (
    PackageManager,
)


class ManifestPackageManagerDetector:

    _RULES = {
        "package.json": "npm",
        "pyproject.toml": "poetry",
        "requirements.txt": "pip",
        "pom.xml": "maven",
        "build.gradle": "gradle",
        "build.gradle.kts": "gradle",
        "Cargo.toml": "cargo",
        "go.mod": "go",
    }

    def detect(
        self,
        dependency_files,
    ):

        managers = set()

        for dependency_file in dependency_files:

            manager_name = (
                self._RULES.get(
                    dependency_file.name,
                )
            )

            if manager_name:

                managers.add(
                    PackageManager(
                        name=manager_name,
                        manifest=(
                            dependency_file.name
                        ),
                    )
                )

        return managers