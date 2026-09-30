import ctypes
from ctypes import wintypes


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("data",)

    _fields_ = [
        ("type", wintypes.DWORD),
        ("data", INPUTUNION),
    ]


class WindowsInput:
    """
    Low-level Windows mouse and keyboard input.
    """

    _KEYS = {
        "BACKSPACE": 0x08,
        "TAB": 0x09,
        "ENTER": 0x0D,
        "SHIFT": 0x10,
        "CTRL": 0x11,
        "ALT": 0x12,
        "ESC": 0x1B,
        "SPACE": 0x20,
        "LEFT": 0x25,
        "UP": 0x26,
        "RIGHT": 0x27,
        "DOWN": 0x28,
        "DELETE": 0x2E,
        "HOME": 0x24,
        "END": 0x23,
        "PAGEUP": 0x21,
        "PAGEDOWN": 0x22,
        "F1": 0x70,
        "F2": 0x71,
        "F3": 0x72,
        "F4": 0x73,
        "F5": 0x74,
        "F6": 0x75,
        "F7": 0x76,
        "F8": 0x77,
        "F9": 0x78,
        "F10": 0x79,
        "F11": 0x7A,
        "F12": 0x7B,
    }

    def __init__(self):
        self._user32 = ctypes.windll.user32

    def move(self, x: int, y: int) -> None:
        if not self._user32.SetCursorPos(
            x,
            y,
        ):
            raise RuntimeError(
                "Windows failed to move the cursor."
            )

    def click(self) -> None:
        self._mouse_button(
            MOUSEEVENTF_LEFTDOWN
        )
        self._mouse_button(
            MOUSEEVENTF_LEFTUP
        )

    def double_click(self) -> None:
        self.click()
        self.click()

    def type_text(self, text: str) -> None:
        for character in text:
            encoded = character.encode(
                "utf-16-le"
            )

            for index in range(
                0,
                len(encoded),
                2,
            ):
                code_unit = int.from_bytes(
                    encoded[index:index + 2],
                    "little",
                )

                self._unicode_key(
                    code_unit,
                    key_up=False,
                )

                self._unicode_key(
                    code_unit,
                    key_up=True,
                )

    def press(self, key: str) -> None:
        normalized = key.upper()

        if len(normalized) == 1:
            virtual_key = ord(normalized)
        else:
            virtual_key = self._KEYS.get(
                normalized
            )

        if virtual_key is None:
            raise ValueError(
                f"unsupported key: {key}"
            )

        self._virtual_key(
            virtual_key,
            key_up=False,
        )

        self._virtual_key(
            virtual_key,
            key_up=True,
        )

    def _mouse_button(
        self,
        flags: int,
    ) -> None:
        input_data = INPUT()

        input_data.type = INPUT_MOUSE

        input_data.mi = MOUSEINPUT(
            0,
            0,
            0,
            flags,
            0,
            None,
        )

        self._send_input(
            input_data
        )

    def _unicode_key(
        self,
        code_unit: int,
        key_up: bool,
    ) -> None:
        flags = KEYEVENTF_UNICODE

        if key_up:
            flags |= KEYEVENTF_KEYUP

        input_data = INPUT()

        input_data.type = INPUT_KEYBOARD

        input_data.ki = KEYBDINPUT(
            0,
            code_unit,
            flags,
            0,
            None,
        )

        self._send_input(
            input_data
        )

    def _virtual_key(
        self,
        virtual_key: int,
        key_up: bool,
    ) -> None:
        flags = KEYEVENTF_KEYUP if key_up else 0

        input_data = INPUT()

        input_data.type = INPUT_KEYBOARD

        input_data.ki = KEYBDINPUT(
            virtual_key,
            0,
            flags,
            0,
            None,
        )

        self._send_input(
            input_data
        )

    def _send_input(
        self,
        input_data: INPUT,
    ) -> None:
        result = self._user32.SendInput(
            1,
            ctypes.byref(input_data),
            ctypes.sizeof(INPUT),
        )

        if result != 1:
            raise RuntimeError(
                "Windows failed to send input."
            )