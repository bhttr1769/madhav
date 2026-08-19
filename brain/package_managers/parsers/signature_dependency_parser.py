from brain.package_managers.models.dependency import (
    Dependency,
)


class SignatureDependencyParser:

    def parse(
        self,
        dependency_file,
    ):

        return {
            Dependency(
                name="fake",
                version="1.0.0",
                source=dependency_file.name,
            )
        }