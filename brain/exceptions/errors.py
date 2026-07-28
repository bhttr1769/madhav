class BrainError(Exception):
    """Base exception for all Brain-related errors."""


class ReaderError(BrainError):
    """Raised when a document cannot be read."""


class ParserError(BrainError):
    """Raised when parsing fails."""


class UnsupportedFileTypeError(BrainError):
    """Raised when no reader exists for a file type."""


class DocumentValidationError(BrainError):
    """Raised when a document is invalid."""