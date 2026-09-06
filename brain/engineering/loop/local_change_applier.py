from pathlib import Path

from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.loop.change_applier import ChangeApplier


class LocalChangeApplier(ChangeApplier):
    def __init__(self, root: str | Path = "."):
        self._root = Path(root).resolve()

    def apply(
        self,
        changes: tuple[CodeChange, ...],
    ) -> None:
        if not isinstance(changes, tuple):
            raise TypeError(
                "changes must be a tuple"
            )

        for change in changes:
            if not isinstance(change, CodeChange):
                raise TypeError(
                    "each change must be a CodeChange"
                )

            path = self._resolve_path(change.path)

            if change.operation == "create":
                self._create(path, change.content)
            elif change.operation == "modify":
                self._modify(path, change.content)
            elif change.operation == "delete":
                self._delete(path)
            else:
                raise ValueError(
                    f"unsupported change operation: "
                    f"{change.operation}"
                )

    def _resolve_path(self, relative_path: str) -> Path:
        path = Path(relative_path)

        if path.is_absolute():
            raise ValueError(
                "change path must be relative"
            )

        resolved = (self._root / path).resolve()

        try:
            resolved.relative_to(self._root)
        except ValueError as exc:
            raise ValueError(
                "change path escapes the configured root"
            ) from exc

        return resolved

    @staticmethod
    def _create(
        path: Path,
        content: str,
    ) -> None:
        if path.exists():
            raise FileExistsError(
                f"file already exists: {path}"
            )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

    @staticmethod
    def _modify(
        path: Path,
        content: str,
    ) -> None:
        if not path.exists():
            raise FileNotFoundError(
                f"file does not exist: {path}"
            )

        if not path.is_file():
            raise IsADirectoryError(
                f"path is not a file: {path}"
            )

        path.write_text(
            content,
            encoding="utf-8",
        )

    @staticmethod
    def _delete(path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(
                f"file does not exist: {path}"
            )

        if not path.is_file():
            raise IsADirectoryError(
                f"path is not a file: {path}"
            )

        path.unlink()