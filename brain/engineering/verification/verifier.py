from brain.environment.models.command import Command
from brain.environment.terminals.local_terminal import LocalTerminal
from brain.engineering.verification.models.verification_request import (
    VerificationRequest,
)
from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)


class Verifier:
    def __init__(self, terminal=None):
        self._terminal = (
            terminal
            if terminal is not None
            else LocalTerminal()
        )

    def verify(
        self,
        request: VerificationRequest,
    ) -> VerificationResult:
        if not isinstance(request, VerificationRequest):
            raise TypeError(
                "request must be a VerificationRequest"
            )

        command = Command(value=request.command)
        result = self._terminal.execute(command)

        return VerificationResult(
            passed=result.return_code == 0,
            return_code=result.return_code,
            stdout=result.stdout,
            stderr=result.stderr,
        )