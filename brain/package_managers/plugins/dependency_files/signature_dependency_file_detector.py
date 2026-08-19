from brain.package_managers.models.dependency_file import (
    DependencyFile,
)


class SignatureDependencyFileDetector:

    def detect(
        self,
        signatures,
    ):

        files = set()

        for signature in signatures:

            if (
                signature.category
                != "filename"
            ):

                continue

            files.add(
                DependencyFile(
                    name=signature.value,
                    path=signature.path,
                    type="manifest",
                )
            )

        return files