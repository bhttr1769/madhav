from brain.evolution.evolution_checkpoint_manager import (
    EvolutionCheckpointManager,
)


class FakeRepository:
    def __init__(self, is_repository=True):
        self.is_repository = is_repository


class FakeBranch:
    def __init__(self, name="main"):
        self.name = name


class FakeStatus:
    def __init__(
        self,
        has_uncommitted_changes=False,
        has_untracked_files=False,
    ):
        self.has_uncommitted_changes = has_uncommitted_changes
        self.has_untracked_files = has_untracked_files


class FakeCommit:
    def __init__(self, hash_value="abc123"):
        self.hash = hash_value


class FakeGitService:
    def __init__(
        self,
        repository=None,
        branch=None,
        status=None,
        commit=None,
    ):
        self._repository = (
            repository
            if repository is not None
            else FakeRepository()
        )
        self._branch = (
            branch
            if branch is not None
            else FakeBranch()
        )
        self._status = (
            status
            if status is not None
            else FakeStatus()
        )
        self._commit = (
            commit
            if commit is not None
            else FakeCommit()
        )

    def repository(self, path):
        return self._repository

    def branch(self, path):
        return self._branch

    def status(self, path):
        return self._status

    def commit(self, path):
        return self._commit


def test_create_produces_active_checkpoint():
    manager = EvolutionCheckpointManager(FakeGitService())

    checkpoint = manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    assert checkpoint.status == EvolutionCheckpointManager.ACTIVE


def test_get_returns_existing_checkpoint():
    manager = EvolutionCheckpointManager(FakeGitService())

    created = manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    retrieved = manager.get("evo-001")

    assert retrieved == created


def test_complete_changes_status_to_completed():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    checkpoint = manager.complete("evo-001")

    assert checkpoint.status == EvolutionCheckpointManager.COMPLETED
    assert manager.get("evo-001").status == EvolutionCheckpointManager.COMPLETED


def test_fail_changes_status_to_failed():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    checkpoint = manager.fail("evo-001")

    assert checkpoint.status == EvolutionCheckpointManager.FAILED
    assert manager.get("evo-001").status == EvolutionCheckpointManager.FAILED


def test_completed_checkpoint_cannot_be_failed():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    manager.complete("evo-001")

    try:
        manager.fail("evo-001")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "completed checkpoint must not be failed"
        )


def test_failed_checkpoint_cannot_be_completed():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    manager.fail("evo-001")

    try:
        manager.complete("evo-001")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "failed checkpoint must not be completed"
        )


def test_completed_checkpoint_cannot_be_completed_again():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    manager.complete("evo-001")

    try:
        manager.complete("evo-001")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "completed checkpoint must not be completed again"
        )


def test_failed_checkpoint_cannot_be_failed_again():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    manager.fail("evo-001")

    try:
        manager.fail("evo-001")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "failed checkpoint must not be failed again"
        )


def test_duplicate_evolution_id_is_rejected():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    try:
        manager.create(
            evolution_id="evo-001",
            repository_path="D:\\Madhav",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "duplicate evolution_id must be rejected"
        )


def test_unknown_evolution_id_is_rejected():
    manager = EvolutionCheckpointManager(FakeGitService())

    try:
        manager.get("evo-999")
    except KeyError:
        pass
    else:
        raise AssertionError(
            "unknown evolution_id must be rejected"
        )

def test_checkpoint_starts_without_evolution_commit():
    manager = EvolutionCheckpointManager(FakeGitService())

    checkpoint = manager.create(
        evolution_id="evo-005",
        repository_path="D:\\Madhav",
    )

    assert checkpoint.evolution_commit_hash is None


def test_sets_evolution_commit():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-006",
        repository_path="D:\\Madhav",
    )

    checkpoint = manager.set_evolution_commit(
        evolution_id="evo-006",
        evolution_commit_hash="def456",
    )

    assert checkpoint.evolution_commit_hash == "def456"
    assert manager.get(
        "evo-006"
    ).evolution_commit_hash == "def456"


def test_rejects_empty_evolution_commit_hash():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-007",
        repository_path="D:\\Madhav",
    )

    try:
        manager.set_evolution_commit(
            evolution_id="evo-007",
            evolution_commit_hash="",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "empty evolution commit hash must be rejected"
        )


def test_rejects_non_string_evolution_commit_hash():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-008",
        repository_path="D:\\Madhav",
    )

    try:
        manager.set_evolution_commit(
            evolution_id="evo-008",
            evolution_commit_hash=123,
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "non-string evolution commit hash must be rejected"
        )


def test_evolution_commit_can_only_be_set_once():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-009",
        repository_path="D:\\Madhav",
    )

    manager.set_evolution_commit(
        evolution_id="evo-009",
        evolution_commit_hash="def456",
    )

    try:
        manager.set_evolution_commit(
            evolution_id="evo-009",
            evolution_commit_hash="ghi789",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "evolution commit must not be changed"
        )


def test_unknown_evolution_cannot_receive_commit():
    manager = EvolutionCheckpointManager(FakeGitService())

    try:
        manager.set_evolution_commit(
            evolution_id="evo-999",
            evolution_commit_hash="def456",
        )
    except KeyError:
        pass
    else:
        raise AssertionError(
            "unknown evolution must be rejected"
        )


def test_completed_checkpoint_cannot_receive_commit():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-010",
        repository_path="D:\\Madhav",
    )

    manager.complete("evo-010")

    try:
        manager.set_evolution_commit(
            evolution_id="evo-010",
            evolution_commit_hash="def456",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "completed checkpoint must not receive an evolution commit"
        )


def test_failed_checkpoint_cannot_receive_commit():
    manager = EvolutionCheckpointManager(FakeGitService())

    manager.create(
        evolution_id="evo-011",
        repository_path="D:\\Madhav",
    )

    manager.fail("evo-011")

    try:
        manager.set_evolution_commit(
            evolution_id="evo-011",
            evolution_commit_hash="def456",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "failed checkpoint must not receive an evolution commit"
        )