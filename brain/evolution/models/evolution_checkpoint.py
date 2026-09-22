from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionCheckpoint:
    evolution_id: str
    repository_path: str
    branch: str
    commit_hash: str
    has_uncommitted_changes: bool
    has_untracked_files: bool
    status: str
    evolution_commit_hash: str | None = None