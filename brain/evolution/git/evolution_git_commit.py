import subprocess


class EvolutionGitCommit:
    def commit(
        self,
        repository_path: str,
        message: str,
        paths: tuple[str, ...],
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
            message,
            str,
        ):
            raise TypeError(
                "message must be a string"
            )

        if not message.strip():
            raise ValueError(
                "message must not be empty"
            )

        if not isinstance(
            paths,
            tuple,
        ):
            raise TypeError(
                "paths must be a tuple"
            )

        if not paths:
            raise ValueError(
                "paths must not be empty"
            )

        for path in paths:
            if not isinstance(path, str):
                raise TypeError(
                    "each path must be a string"
                )

            if not path.strip():
                raise ValueError(
                    "paths must not contain empty values"
                )

        add_result = subprocess.run(
            [
                "git",
                "add",
                "--",
                *paths,
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        if add_result.returncode != 0:
            raise RuntimeError(
                "git add failed: "
                f"{add_result.stderr.strip()}"
            )

        commit_result = subprocess.run(
            [
                "git",
                "commit",
                "-m",
                message,
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        if commit_result.returncode != 0:
            raise RuntimeError(
                "git commit failed: "
                f"{commit_result.stderr.strip()}"
            )

        hash_result = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        if hash_result.returncode != 0:
            raise RuntimeError(
                "failed to determine evolution commit hash: "
                f"{hash_result.stderr.strip()}"
            )

        commit_hash = hash_result.stdout.strip()

        if not commit_hash:
            raise RuntimeError(
                "evolution commit hash must not be empty"
            )

        return commit_hash