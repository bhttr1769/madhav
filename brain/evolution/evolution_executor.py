from brain.capabilities.capability_discovery import (
    CapabilityDiscovery,
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

        if mode is EvolutionMode.AUTONOMOUS:
            if not isinstance(
                integration_request,
                EvolutionDiscoveryRequest,
            ):
                raise TypeError(
                    "autonomous execution requires an "
                    "EvolutionDiscoveryRequest"
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

        task_results = []

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

        if not self._policy.allows_verification(
            mode
        ):
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
            self._integrate(
                integration_request
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