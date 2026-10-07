from dataclasses import dataclass


@dataclass(frozen=True)
class ContextValidation:
    valid: bool
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.valid, bool):
            raise TypeError("valid must be a boolean")

        if not isinstance(self.errors, tuple):
            raise TypeError("errors must be a tuple")

        for error in self.errors:
            if not isinstance(error, str):
                raise TypeError("errors must contain only strings")