from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    """
    Represents an HTTP response.
    """

    url: str

    status_code: int

    content: str