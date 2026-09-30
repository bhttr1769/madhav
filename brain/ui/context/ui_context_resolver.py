from abc import ABC, abstractmethod
import os
import subprocess


class UIContextResolver(ABC):
    """
    Resolves the application and window context
    associated with the currently focused UI control.
    """

    @abstractmethod
    def resolve(self) -> tuple[str | None, str | None]:
        """
        Return (application, window_title).
        """
        raise NotImplementedError


class WindowsUIContextResolver(UIContextResolver):
    """
    Resolves the current Windows UI context using UI Automation.
    """

    def __init__(self, automation=None):
        if automation is None:
            try:
                import uiautomation
            except ImportError as error:
                raise RuntimeError(
                    "uiautomation is required for Windows UI context resolution"
                ) from error

            automation = uiautomation

        self._automation = automation

    def resolve(self) -> tuple[str | None, str | None]:
        focused_control = (
            self._automation.GetFocusedControl()
        )

        if focused_control is None:
            return None, None

        window_control = self._find_window_ancestor(
            focused_control
        )

        if window_control is None:
            return None, None

        window_title = self._get_control_name(
            window_control
        )

        process_id = self._get_process_id(
            focused_control
        )

        application = self._resolve_process_name(
            process_id
        )

        return application, window_title

    def _find_window_ancestor(self, control):
        current = control

        while current is not None:

            if self._is_window_control(current):
                return current

            current = self._get_parent(current)

        return None

    def _is_window_control(self, control) -> bool:
        control_type = getattr(
            control,
            "ControlType",
            None,
        )

        window_control_type = getattr(
            self._automation.ControlType,
            "WindowControl",
            None,
        )

        return (
            control_type == window_control_type
        )

    @staticmethod
    def _get_parent(control):
        try:
            return control.GetParentControl()
        except Exception:
            return None

    @staticmethod
    def _get_control_name(control):
        try:
            name = control.Name
        except Exception:
            return None

        if not name:
            return None

        return str(name)

    @staticmethod
    def _get_process_id(control):
        try:
            process_id = control.ProcessId
        except Exception:
            return None

        if not process_id:
            return None

        return int(process_id)

    @staticmethod
    def _resolve_process_name(
        process_id: int | None,
    ) -> str | None:

        if process_id is None:
            return None

        try:
            result = subprocess.run(
                [
                    "tasklist",
                    "/FI",
                    f"PID eq {process_id}",
                    "/FO",
                    "CSV",
                    "/NH",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return None

        if result.returncode != 0:
            return None

        output = result.stdout.strip()

        if not output:
            return None

        first_line = output.splitlines()[0].strip()

        if not first_line:
            return None

        # tasklist CSV output:
        # "Image Name","PID","Session Name",...
        if first_line.startswith('"'):
            end_quote = first_line.find(
                '"',
                1,
            )

            if end_quote > 1:
                return first_line[
                    1:end_quote
                ]

        return first_line.split(",")[0].strip(
            '" '
        )