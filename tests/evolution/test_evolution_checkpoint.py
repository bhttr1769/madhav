from brain.evolution.evolution_checkpoint import EvolutionCheckpointManager
from brain.evolution.models.evolution_checkpoint import EvolutionCheckpoint


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


def test_creates_evolution_checkpoint():
    manager = EvolutionCheckpointManager(FakeGitService())

    checkpoint = manager.create(
        evolution_id="evo-001",
        repository_path="D:\\Madhav",
    )

    assert isinstance(checkpoint, EvolutionCheckpoint)
    assert checkpoint.evolution_id == "evo-001"
    assert checkpoint.repository_path == "D:\\Madhav"
    assert checkpoint.branch == "main"
    assert checkpoint.commit_hash == "abc123"
    assert checkpoint.has_uncommitted_changes is False
    assert checkpoint.has_untracked_files is False
    assert checkpoint.status == "active"


def test_captures_dirty_repository_state():
    manager = EvolutionCheckpointManager(
        FakeGitService(
            status=FakeStatus(
                has_uncommitted_changes=True,
                has_untracked_files=True,
            )
        )
    )

    checkpoint = manager.create(
        evolution_id="evo-002",
        repository_path="D:\\Madhav",
    )

    assert checkpoint.has_uncommitted_changes is True
    assert checkpoint.has_untracked_files is True
    assert checkpoint.status == "active"


def test_rejects_non_repository():
    manager = EvolutionCheckpointManager(
        FakeGitService(
            repository=FakeRepository(is_repository=False)
        )
    )

    try:
        manager.create(
            evolution_id="evo-003",
            repository_path="D:\\Madhav",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "non-repository path must be rejected"
        )


def test_rejects_empty_evolution_id():
    manager = EvolutionCheckpointManager(FakeGitService())

    try:
        manager.create(
            evolution_id="",
            repository_path="D:\\Madhav",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "empty evolution_id must be rejected"
        )


def test_rejects_empty_repository_path():
    manager = EvolutionCheckpointManager(FakeGitService())

    try:
        manager.create(
            evolution_id="evo-004",
            repository_path="",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "empty repository path must be rejected"
        )