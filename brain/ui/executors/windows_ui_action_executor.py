from brain.ui.executors.ui_action_executor import (
    UIActionExecutor,
)

from brain.ui.executors.windows_input import (
    WindowsInput,
)

from brain.ui.models.ui_action import (
    UIAction,
)


class WindowsUIActionExecutor(
    UIActionExecutor,
):
    """
    Executes UI actions using Windows input APIs.
    """

    def __init__(
        self,
        input_controller: WindowsInput | None = None,
    ):
        self._input = (
            input_controller
            if input_controller is not None
            else WindowsInput()
        )

    def execute(
        self,
        action: UIAction,
    ) -> None:

        if not isinstance(
            action,
            UIAction,
        ):
            raise TypeError(
                "action must be a UIAction"
            )

        if action.action_type == "click":
            self._move_to_action_target(
                action
            )
            self._input.click()
            return

        if action.action_type == "double_click":
            self._move_to_action_target(
                action
            )
            self._input.double_click()
            return

        if action.action_type == "move":
            self._move_to_action_target(
                action
            )
            return

        if action.action_type == "type":
            self._input.type_text(
                action.text
            )
            return

        if action.action_type == "press":
            self._input.press(
                action.key
            )
            return

        raise ValueError(
            f"unsupported UI action type: "
            f"{action.action_type}"
        )

    def _move_to_action_target(
        self,
        action: UIAction,
    ) -> None:

        if action.target is not None:
            x = (
                action.target.x
                + action.target.width // 2
            )
            y = (
                action.target.y
                + action.target.height // 2
            )

        else:
            x = action.x
            y = action.y

        if x is None or y is None:
            raise ValueError(
                "UI action has no executable coordinates"
            )

        self._input.move(
            x,
            y,
        )