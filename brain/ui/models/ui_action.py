from dataclasses import dataclass

from brain.safety.models.action import (
    Action,
)

from brain.ui.models.ui_element import (
    UIElement,
)


@dataclass(frozen=True)
class UIAction:
    """
    Represents a desktop user-interface action.

    This model describes an intended UI operation.
    It does not execute the operation.
    """

    action_type: str

    target: UIElement | None = None

    x: int | None = None

    y: int | None = None

    text: str | None = None

    key: str | None = None

    _SUPPORTED_ACTIONS = frozenset(
        {
            "click",
            "double_click",
            "move",
            "type",
            "press",
        }
    )

    def __post_init__(self):

        if not isinstance(
            self.action_type,
            str,
        ):
            raise TypeError(
                "action_type must be a string"
            )

        if self.action_type not in (
            self._SUPPORTED_ACTIONS
        ):
            raise ValueError(
                "unsupported UI action type: "
                f"{self.action_type}"
            )

        if self.target is not None and not isinstance(
            self.target,
            UIElement,
        ):
            raise TypeError(
                "target must be a UIElement or None"
            )

        if self.x is not None and not isinstance(
            self.x,
            int,
        ):
            raise TypeError(
                "x must be an integer or None"
            )

        if self.y is not None and not isinstance(
            self.y,
            int,
        ):
            raise TypeError(
                "y must be an integer or None"
            )

        if self.text is not None and not isinstance(
            self.text,
            str,
        ):
            raise TypeError(
                "text must be a string or None"
            )

        if self.key is not None and not isinstance(
            self.key,
            str,
        ):
            raise TypeError(
                "key must be a string or None"
            )

        if self.action_type in {
            "click",
            "double_click",
            "move",
        }:
            if self.target is None and (
                self.x is None
                or self.y is None
            ):
                raise ValueError(
                    "UI action requires a target "
                    "or both x and y coordinates"
                )

        if self.action_type == "type":
            if self.text is None:
                raise ValueError(
                    "type action requires text"
                )

        if self.action_type == "press":
            if self.key is None:
                raise ValueError(
                    "press action requires key"
                )

    def to_action(self) -> Action:
        """
        Converts the UI action into the existing
        safety-layer Action representation.
        """

        target = self._target_description()

        return Action(
            name=self.action_type,
            category="ui",
            target=target,
        )

    def _target_description(self) -> str:

        parts = []

        if self.target is not None:
            parts.append(
                "element="
                f"{self.target.element_type}:"
                f"{self.target.name}"
            )

            parts.append(
                "bounds="
                f"{self.target.x},"
                f"{self.target.y},"
                f"{self.target.width},"
                f"{self.target.height}"
            )

        if self.x is not None:
            parts.append(
                f"x={self.x}"
            )

        if self.y is not None:
            parts.append(
                f"y={self.y}"
            )

        if self.text is not None:
            parts.append(
                f"text={self.text!r}"
            )

        if self.key is not None:
            parts.append(
                f"key={self.key}"
            )

        return ";".join(parts)