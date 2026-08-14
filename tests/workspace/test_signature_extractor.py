from pathlib import Path

from brain.workspace.extraction.signature_extractor import (
    SignatureExtractor,
)


def test_signature_extractor():

    files = [
        Path("src/main.py"),
        Path("docs/README.md"),
    ]

    signatures = (
        SignatureExtractor()
    ).extract(files)

    assert len(signatures) > 0

    assert any(
        signature.value == ".py"
        for signature in signatures
    )

    assert any(
        signature.value == "main.py"
        for signature in signatures
    )

    assert any(
        signature.value == "src"
        for signature in signatures
    )