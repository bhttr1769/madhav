import hashlib

from brain.models.document import Document


def create_fingerprint(
    document: Document,
) -> str:
    """
    Create a stable fingerprint for a document.
    """

    return hashlib.sha256(
        document.content.encode(
            "utf-8"
        )
    ).hexdigest()