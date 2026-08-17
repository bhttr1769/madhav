import platform

from brain.environment.models.operating_system import (
    OperatingSystem,
)


class OSDetector:
    """
    Detects the current operating system.
    """

    def detect(
        self,
    ):

        return OperatingSystem(
            name=platform.system(),
            version=platform.version(),
        )