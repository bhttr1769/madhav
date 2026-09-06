from brain.engineering.debugging.models.debugging_request import (
    DebuggingRequest,
)
from brain.engineering.improvement.models.engineering_improvement_request import (
    EngineeringImprovementRequest,
)
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)
from brain.engineering.loop.models.engineering_loop_request import (
    EngineeringLoopRequest,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.engineering.refactoring.models.refactoring_request import (
    RefactoringRequest,
)
from brain.engineering.verification.models.verification_assessment import (
    VerificationAssessment,
)
from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)
from brain.engineering.verification.verification_interpreter import (
    VerificationInterpreter,
)
from brain.engineering.loop.local_change_applier import (
    LocalChangeApplier,
)


class EngineeringLoop:
    def __init__(
        self,
        verifier,
        debugger,
        refactorer,
        improver,
        change_applier=None,
        interpreter=None,
    ):
        self._verifier = verifier
        self._debugger = debugger
        self._refactorer = refactorer
        self._improver = improver
        self._change_applier = (
            change_applier
            if change_applier is not None
            else LocalChangeApplier()
        )
        self._interpreter = (
            interpreter
            if interpreter is not None
            else VerificationInterpreter
        )

    def execute(
        self,
        request: EngineeringLoopRequest,
    ) -> EngineeringLoopResult:
        if not isinstance(
            request,
            EngineeringLoopRequest,
        ):
            raise TypeError(
                "request must be an EngineeringLoopRequest"
            )

        if request.max_iterations < 1:
            raise ValueError(
                "max_iterations must be at least 1"
            )

        accumulated_changes = list(
            request.proposed_changes
        )
        iterations = []

        for iteration_number in range(
            1,
            request.max_iterations + 1,
        ):
            verification_result = (
                self._verify(
                    request,
                    accumulated_changes,
                )
            )

            assessment = self._interpret(
                verification_result
            )

            if assessment.passed:
                iterations.append(
                    EngineeringLoopIteration(
                        iteration=iteration_number,
                        changes=tuple(
                            accumulated_changes
                        ),
                        passed=True,
                        summary=assessment.summary,
                    )
                )

                return EngineeringLoopResult(
                    changes=tuple(
                        accumulated_changes
                    ),
                    passed=True,
                    iterations=tuple(iterations),
                    termination_reason=(
                        "verification_passed"
                    ),
                )

            iteration_changes = []

            debug_changes = self._debug(
                request,
                accumulated_changes,
                assessment,
            )

            self._apply_changes(debug_changes)

            accumulated_changes.extend(
                debug_changes
            )
            iteration_changes.extend(
                debug_changes
            )

            refactor_changes = self._refactor(
                request,
                accumulated_changes,
            )

            self._apply_changes(
                refactor_changes
            )

            accumulated_changes.extend(
                refactor_changes
            )
            iteration_changes.extend(
                refactor_changes
            )

            improvement_changes = self._improve(
                request,
                accumulated_changes,
            )

            self._apply_changes(
                improvement_changes
            )

            accumulated_changes.extend(
                improvement_changes
            )
            iteration_changes.extend(
                improvement_changes
            )

            iterations.append(
                EngineeringLoopIteration(
                    iteration=iteration_number,
                    changes=tuple(
                        iteration_changes
                    ),
                    passed=False,
                    summary=assessment.summary,
                )
            )

        return EngineeringLoopResult(
            changes=tuple(accumulated_changes),
            passed=False,
            iterations=tuple(iterations),
            termination_reason=(
                "max_iterations_reached"
            ),
        )

    def _verify(
        self,
        request: EngineeringLoopRequest,
        accumulated_changes,
    ) -> VerificationResult:
        return self._verifier.verify(
            self._build_verification_request(
                request,
                accumulated_changes,
            )
        )

    def _interpret(
        self,
        result: VerificationResult,
    ) -> VerificationAssessment:
        return self._interpreter.interpret(result)

    def _debug(
        self,
        request: EngineeringLoopRequest,
        accumulated_changes,
        assessment: VerificationAssessment,
    ):
        debug_request = DebuggingRequest(
            task=request.task,
            design=request.design,
            plan=request.plan,
            existing_code=request.existing_code,
            proposed_changes=tuple(
                accumulated_changes
            ),
            error_message=assessment.summary,
            traceback=assessment.failure_output,
        )

        result = self._debugger.debug(
            debug_request
        )

        return result.changes

    def _refactor(
        self,
        request: EngineeringLoopRequest,
        accumulated_changes,
    ):
        refactoring_request = RefactoringRequest(
            task=request.task,
            design=request.design,
            plan=request.plan,
            existing_code=request.existing_code,
            proposed_changes=tuple(
                accumulated_changes
            ),
        )

        result = self._refactorer.refactor(
            refactoring_request
        )

        return result.changes

    def _improve(
        self,
        request: EngineeringLoopRequest,
        accumulated_changes,
    ):
        improvement_request = (
            EngineeringImprovementRequest(
                task=request.task,
                design=request.design,
                plan=request.plan,
                existing_code=request.existing_code,
                proposed_changes=tuple(
                    accumulated_changes
                ),
            )
        )

        result = self._improver.improve(
            improvement_request
        )

        return result.changes

    def _apply_changes(self, changes):
        if changes:
            self._change_applier.apply(
                tuple(changes)
            )

    @staticmethod
    def _build_verification_request(
        request: EngineeringLoopRequest,
        accumulated_changes,
    ):
        from brain.engineering.verification.models.verification_request import (
            VerificationRequest,
        )

        return VerificationRequest(
            task=request.task,
            plan=request.plan,
            existing_code=request.existing_code,
            proposed_changes=tuple(
                accumulated_changes
            ),
            command=request.verification_command,
        )