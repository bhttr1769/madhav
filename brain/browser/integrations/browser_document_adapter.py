from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from brain.models.document import Document


class BrowserDocumentAdapter:
    """
    Converts browser-acquired content into Madhav's canonical Document model.
    """

    def to_document(
        self,
        url: str,
        content: str,
        acquired_at: datetime | None = None,
    ) -> Document:
        if not isinstance(url, str):
            raise TypeError("url must be a string")

        if not url.strip():
            raise ValueError("url must not be empty")

        if not isinstance(content, str):
            raise TypeError("content must be a string")

        if acquired_at is not None and not isinstance(
            acquired_at,
            datetime,
        ):
            raise TypeError("acquired_at must be a datetime or None")

        normalized_url = url.strip()
        parsed = urlparse(normalized_url)

        if not parsed.scheme or not parsed.netloc:
            raise ValueError("url must contain a valid scheme and host")

        timestamp = (
            acquired_at
            if acquired_at is not None
            else datetime.now()
        )

        name = parsed.path.rstrip("/").split("/")[-1]

        if not name:
            name = parsed.netloc

        if "." not in name:
            name = f"{name}.html"

        return Document(
            name=name,
            path=Path(f"browser://{normalized_url}"),
            extension=".html",
            content=content,
            size=len(content.encode("utf-8")),
            created_at=timestamp,
            modified_at=timestamp,
            language="unknown",
            source="browser",
            metadata={
                "source_url": normalized_url,
            },
        )