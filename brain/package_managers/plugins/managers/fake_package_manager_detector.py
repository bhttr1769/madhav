from brain.package_managers.models.package_manager import (
    PackageManager,
)


class FakePackageManagerDetector:

    def detect(
        self,
        signatures,
    ):

        return {
            PackageManager(
                name="FakePackageManager",
                manifest="fake.manifest",
            )
        }