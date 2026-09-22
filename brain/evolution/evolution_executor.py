from datetime import datetime

from brain.evolution.evolution_history_recorder import (
    EvolutionHistoryRecorder,
)
from brain.evolution.evolution_id_generator import (
    EvolutionIdGenerator,
)
from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)
from brain.evolution.evolution_history_builder import (
    EvolutionHistoryBuilder,
)

from brain.capabilities.capability_discovery import (
    CapabilityDiscovery,
)
from brain.evolution.evolution_checkpoint import (
    EvolutionCheckpointManager,
)
from brain.evolution.evolution_failure_policy import (
    EvolutionFailurePolicy,
)
from brain.evolution.evolution_policy import (
    EvolutionPolicy,
)
from brain.evolution.evolution_task_executor import (
    EvolutionTaskExecutor,
)
from brain.evolution.evolution_task_sequencer import (
    EvolutionTaskSequencer,
)
from brain.evolution.evolution_integration_recovery_coordinator import (
    EvolutionIntegrationRecoveryCoordinator,
)
from brain.evolution.git.evolution_git_commit import (
    EvolutionGitCommit,
)
from brain.evolution.models.evolution_discovery_request import (
    EvolutionDiscoveryRequest,
)
from brain.evolution.models.evolution_mode import (
    EvolutionMode,
)
from brain.evolution.models.evolution_proposal import (
    EvolutionProposal,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)
from brain.evolution.models.evolution_result import (
    EvolutionResult,
)
from brain.evolution.evolution_safety_policy import (
    EvolutionSafetyPolicy,
)


class EvolutionExecutor:
    def __init__(
        self,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        engineering_generation,
        test_generator,
        engineering_loop,
        existing_code,
        verification_command,
        max_iterations=3,
        policy=None,
        discovery=None,
        capability_integrator=None,
        task_sequencer=None,
        task_executor=None,
        failure_policy=None,
        history_recorder=None,
        evolution_id_generator=None,
        history_builder=None,
        checkpoint_manager=None,
        evolution_git_commit=None,
        integration_recovery_coordinator=None,
        safety_policy=None,
    ):
        self._requirement_service = requirement_service
        self._task_decomposer = task_decomposer
        self._system_designer = system_designer
        self._planner = planner
        self._engineering_generation = (
            engineering_generation
        )
        self._test_generator = test_generator
        self._engineering_loop = engineering_loop
        self._existing_code = existing_code
        self._verification_command = (
            verification_command
        )
        self._max_iterations = max_iterations

        self._policy = (
            policy
            if policy is not None
            else EvolutionPolicy()
        )

        self._discovery = (
            discovery
            if discovery is not None
            else CapabilityDiscovery()
        )

        self._capability_integrator = (
            capability_integrator
            if capability_integrator is not None
            else None
        )

        self._task_sequencer = (
            task_sequencer
            if task_sequencer is not None
            else EvolutionTaskSequencer()
        )

        self._task_executor = (
            task_executor
            if task_executor is not None
            else EvolutionTaskExecutor(
                engineering_generation=(
                    engineering_generation
                ),
                test_generator=test_generator,
                engineering_loop=engineering_loop,
                existing_code=existing_code,
                verification_command=(
                    verification_command
                ),
                max_iterations=max_iterations,
            )
        )

        self._failure_policy = (
            failure_policy
            if failure_policy is not None
            else EvolutionFailurePolicy()
        )

        self._history_recorder = (
            history_recorder
            if history_recorder is not None
            else EvolutionHistoryRecorder()
        )

        self._evolution_id_generator = (
            evolution_id_generator
            if evolution_id_generator is not None
            else EvolutionIdGenerator()
        )

        self._history_builder = (
            history_builder
            if history_builder is not None
            else EvolutionHistoryBuilder()
        )

        self._checkpoint_manager = (
            checkpoint_manager
        )

        self._evolution_git_commit = (
            evolution_git_commit
        )

        self._integration_recovery_coordinator = (
            integration_recovery_coordinator
        )

        self._safety_policy = (
            safety_policy
            if safety_policy is not None
            else EvolutionSafetyPolicy()
        )

    def propose(
        self,
        request: EvolutionRequest,
    ) -> EvolutionProposal:
        if not isinstance(
            request,
            EvolutionRequest,
        ):
            raise TypeError(
                "request must be an EvolutionRequest"
            )

        mode = EvolutionMode(request.mode)

        if mode is not EvolutionMode.PROPOSAL:
            raise ValueError(
                "propose() requires proposal mode"
            )

        (
            requirement,
            decomposition,
            design,
            plan,
        ) = self._prepare(request)

        return EvolutionProposal(
            requested_capability=(
                request.requested_capability
            ),
            requirement=requirement,
            task_decomposition=decomposition,
            design=design,
            plan=plan,
        )

    def execute(
        self,
        request: EvolutionRequest,
        integration_request=None,
    ) -> EvolutionResult:
        if not isinstance(
            request,
            EvolutionRequest,
        ):
            raise TypeError(
                "request must be an EvolutionRequest"
            )

        mode = EvolutionMode(request.mode)

        if mode is EvolutionMode.PROPOSAL:
            raise ValueError(
                "proposal mode requires propose(), "
                "not execute()"
            )

        evolution_id = (
            self._evolution_id_generator.generate()
        )

        started_at = datetime.now()

        if mode is EvolutionMode.AUTONOMOUS:
            if not isinstance(
                integration_request,
                EvolutionDiscoveryRequest,
            ):
                raise TypeError(
                    "autonomous execution requires an "
                    "EvolutionDiscoveryRequest"
                )

            if self._checkpoint_manager is None:
                raise RuntimeError(
                    "autonomous execution requires "
                    "an EvolutionCheckpointManager"
                )

            if self._evolution_git_commit is None:
                raise RuntimeError(
                    "autonomous execution requires "
                    "an EvolutionGitCommit"
                )

            if (
                self._integration_recovery_coordinator
                is None
            ):
                raise RuntimeError(
                    "autonomous execution requires "
                    "an integration recovery coordinator"
                )

        elif integration_request is not None:
            raise ValueError(
                "integration_request is only valid "
                "for autonomous mode"
            )

        (
            requirement,
            decomposition,
            design,
            plan,
        ) = self._prepare(request)

        if not self._policy.allows_implementation(
            mode
        ):
            raise ValueError(
                "evolution mode does not allow "
                "implementation"
            )

        tasks = self._task_sequencer.sequence(
            decomposition.tasks
        )

        if not tasks:
            raise ValueError(
                "task decomposition must contain "
                "at least one task"
            )

        checkpoint = None

        if mode is EvolutionMode.AUTONOMOUS:
            checkpoint = (
                self._checkpoint_manager.create(
                    evolution_id=evolution_id,
                    repository_path=(
                        integration_request.repository_path
                    ),
                )
            )

            try:
                self._safety_policy.validate_autonomous_execution(
                checkpoint
            )
            except Exception:
                self._checkpoint_manager.fail(
                evolution_id
            )
                raise

        task_results = []

        try:
            for task in tasks:
                task_result = self._task_executor.execute(
                    task=task,
                    design=design,
                    plan=plan,
                    task_id=task.id,
                )

                task_results.append(
                    task_result
                )

                if self._failure_policy.should_stop(
                    task_result
                ):
                    break

        except Exception:
            if checkpoint is not None:
                self._checkpoint_manager.fail(
                    evolution_id
                )

            raise

        if not self._policy.allows_verification(
            mode
        ):
            if checkpoint is not None:
                self._checkpoint_manager.fail(
                    evolution_id
                )

            raise ValueError(
                "evolution mode does not allow "
                "verification"
            )

        task_results_tuple = tuple(
            task_results
        )

        proposed_changes = tuple(
            change
            for task_result in task_results_tuple
            for change in task_result.proposed_changes
        )

        engineering_result = (
            task_results_tuple[-1].engineering_result
        )

        evolution_result = EvolutionResult(
            requested_capability=(
                request.requested_capability
            ),
            requirement=requirement,
            task_decomposition=decomposition,
            design=design,
            plan=plan,
            proposed_changes=proposed_changes,
            engineering_result=engineering_result,
            task_results=task_results_tuple,
        )

        if (
            mode is EvolutionMode.AUTONOMOUS
            and evolution_result.passed
        ):
            changed_paths = tuple(
                dict.fromkeys(
                    change.path
                    for change in proposed_changes
                )
            )

            if not changed_paths:
                self._checkpoint_manager.fail(
                    evolution_id
                )

                raise RuntimeError(
                    "autonomous evolution produced "
                    "no changes to commit"
                )

            try:
                evolution_commit_hash = (
                    self._evolution_git_commit.commit(
                        repository_path=(
                            integration_request.repository_path
                        ),
                        paths=changed_paths,
                        message=(
                            "evolution: "
                            f"{request.requested_capability}"
                        ),
                    )
                )

                checkpoint = (
                    self._checkpoint_manager.set_evolution_commit(
                        evolution_id,
                        evolution_commit_hash,
                    )
                )

            except Exception:
                self._checkpoint_manager.fail(
                    evolution_id
                )

                raise

        if (
            mode is EvolutionMode.AUTONOMOUS
            and evolution_result.passed
        ):
            try:
                self._integrate(
                    integration_request
                )

            except Exception as exc:
                if checkpoint is not None:
                    self._integration_recovery_coordinator.recover(
                        checkpoint=checkpoint,
                        reason=str(exc),
                    )

                    self._checkpoint_manager.fail(
                        evolution_id
                    )

                completed_at = datetime.now()

                history = self._history_builder.build(
                    evolution_id=evolution_id,
                    request=request,
                    result=evolution_result,
                    started_at=started_at,
                    completed_at=completed_at,
                    status="failed",
                )

                self._history_recorder.record(
                    history
                )

                raise

            self._checkpoint_manager.complete(
                evolution_id
            )

        elif checkpoint is not None:
            self._checkpoint_manager.fail(
                evolution_id
            )

        completed_at = datetime.now()

        history = self._history_builder.build(
            evolution_id=evolution_id,
            request=request,
            result=evolution_result,
            started_at=started_at,
            completed_at=completed_at,
            status=(
                "completed"
                if evolution_result.passed
                else "failed"
            ),
        )

        self._history_recorder.record(
            history
        )

        return evolution_result

    def _integrate(
        self,
        discovery_request: EvolutionDiscoveryRequest,
    ) -> None:
        if not isinstance(
            discovery_request,
            EvolutionDiscoveryRequest,
        ):
            raise TypeError(
                "discovery_request must be an "
                "EvolutionDiscoveryRequest"
            )

        if self._capability_integrator is None:
            raise RuntimeError(
                "autonomous integration requires "
                "a CapabilityIntegrator"
            )

        capabilities = self._discovery.discover(
            providers=(
                discovery_request.provider,
            ),
        )

        if not capabilities:
            raise ValueError(
                "evolved provider did not expose "
                "a capability descriptor"
            )

        if len(capabilities) != 1:
            raise ValueError(
                "evolved provider must expose exactly "
                "one capability"
            )

        self._capability_integrator.integrate(
            capability=capabilities[0],
            verification_passed=True,
        )

    def _prepare(
        self,
        request: EvolutionRequest,
    ):
        requirement = (
            self._requirement_service.understand(
                request.objective,
            )
        )

        decomposition = (
            self._task_decomposer.decompose(
                requirement,
            )
        )

        design = self._system_designer.design(
            decomposition,
        )

        plan = self._planner.plan(
            decomposition,
        )

        return (
            requirement,
            decomposition,
            design,
            plan,
        )