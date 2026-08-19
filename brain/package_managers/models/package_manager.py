from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class PackageManager:
    """
    Represents a package manager.
    """

    name: str
    manifest: str