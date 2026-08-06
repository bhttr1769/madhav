class DuplicateNodeError(Exception):
    """Raised when a node with the same ID already exists."""


class DuplicateEdgeError(Exception):
    """Raised when an edge with the same ID already exists."""