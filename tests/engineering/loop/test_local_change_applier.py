from pathlib import Path

import pytest

from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.loop.local_change_applier import (
    LocalChangeApplier,
)


def test_create_change_creates_file(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="brain/example.py",
        operation="create",
        content="return_value = 1",
    )

    applier.apply((change,))

    path = tmp_path / "brain" / "example.py"

    assert path.exists()
    assert path.read_text(encoding="utf-8") == (
        "return_value = 1"
    )


def test_modify_change_updates_file(tmp_path):
    path = tmp_path / "brain" / "example.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "return_value = 1",
        encoding="utf-8",
    )

    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="brain/example.py",
        operation="modify",
        content="return_value = 2",
    )

    applier.apply((change,))

    assert path.read_text(encoding="utf-8") == (
        "return_value = 2"
    )


def test_delete_change_removes_file(tmp_path):
    path = tmp_path / "brain" / "example.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "obsolete",
        encoding="utf-8",
    )

    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="brain/example.py",
        operation="delete",
        content="",
    )

    applier.apply((change,))

    assert not path.exists()


def test_create_change_rejects_existing_file(tmp_path):
    path = tmp_path / "example.py"
    path.write_text(
        "existing",
        encoding="utf-8",
    )

    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="example.py",
        operation="create",
        content="new",
    )

    with pytest.raises(FileExistsError):
        applier.apply((change,))


def test_modify_change_rejects_missing_file(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="missing.py",
        operation="modify",
        content="new",
    )

    with pytest.raises(FileNotFoundError):
        applier.apply((change,))


def test_delete_change_rejects_missing_file(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="missing.py",
        operation="delete",
        content="",
    )

    with pytest.raises(FileNotFoundError):
        applier.apply((change,))


def test_applier_rejects_absolute_path(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path=str(Path(tmp_path) / "unsafe.py"),
        operation="create",
        content="unsafe",
    )

    with pytest.raises(ValueError):
        applier.apply((change,))


def test_applier_rejects_path_traversal(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="../unsafe.py",
        operation="create",
        content="unsafe",
    )

    with pytest.raises(ValueError):
        applier.apply((change,))


def test_applier_rejects_non_tuple_changes(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="example.py",
        operation="create",
        content="content",
    )

    with pytest.raises(TypeError):
        applier.apply([change])


def test_applier_rejects_invalid_change(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    with pytest.raises(TypeError):
        applier.apply(("invalid",))


def test_applier_rejects_unknown_operation(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="example.py",
        operation="rename",
        content="content",
    )

    with pytest.raises(ValueError):
        applier.apply((change,))


def test_applier_creates_parent_directories(tmp_path):
    applier = LocalChangeApplier(tmp_path)

    change = CodeChange(
        path="nested/deep/example.py",
        operation="create",
        content="content",
    )

    applier.apply((change,))

    assert (
        tmp_path
        / "nested"
        / "deep"
        / "example.py"
    ).exists()