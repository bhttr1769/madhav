from pathlib import Path

from brain.workspace.models.signature import (
    Signature,
)


class SignatureExtractor:
    """
    Extracts signatures from a workspace.
    """

    def extract(
        self,
        files: list[Path],
    ) -> set[Signature]:

        signatures = set()

        for file in files:

            signatures.add(
                Signature(
                    value=file.name,
                    category="filename",
                )
            )

            if file.suffix:

                signatures.add(
                    Signature(
                        value=file.suffix.lower(),
                        category="extension",
                    )
                )

            for parent in file.parents:

                if str(parent) != ".":

                    signatures.add(
                        Signature(
                            value=str(parent),
                            category="directory",
                        )
                    )

        return signatures