from dataclasses import dataclass


@dataclass(frozen=True)
class DelegationScope:
    """Explicit action and target boundaries for delegated authority."""

    actions: tuple[str, ...]
    targets: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("actions", "targets"):
            values = getattr(self, field_name)

            if not isinstance(values, tuple):
                raise TypeError(f"{field_name} must be a tuple")

            if not values:
                raise ValueError(f"{field_name} must not be empty")

            for value in values:
                if not isinstance(value, str):
                    raise TypeError(
                        f"each {field_name} entry must be a string"
                    )

                if not value.strip():
                    raise ValueError(
                        f"{field_name} entries must not be empty"
                    )

                if value.strip() == "*":
                    raise ValueError(
                        f"{field_name} must use explicit values, not '* '"
                    )

            if len(set(values)) != len(values):
                raise ValueError(
                    f"{field_name} must not contain duplicates"
                )