import subprocess


class EvolutionGitRollback:
    def revert(
        self,
        repository_path: str,
        commit_hash: str,
    ) -> str:
        if not isinstance(
            repository_path,
            str,
        ):
            raise TypeError(
                "repository_path must be a string"
            )

        if not repository_path.strip():
            raise ValueError(
                "repository_path must not be empty"
            )

        if not isinstance(
            commit_hash,
            str,
        ):
            raise TypeError(
                "commit_hash must be a string"
            )

        if not commit_hash.strip():
            raise ValueError(
                "commit_hash must not be empty"
            )

        result = subprocess.run(
            [
                "git",
                "revert",
                "--no-edit",
                commit_hash,
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "git revert failed: "
                f"{result.stderr.strip()}"
            )

        return result.stdout.strip()