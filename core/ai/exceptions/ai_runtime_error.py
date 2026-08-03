class AIRuntimeError(Exception):
    """
    Base class for all AI Runtime exceptions.
    """

    def __init__(self, message: str):
        super().__init__(message)