from brain.capabilities.capability_discovery import (
    CapabilityDiscovery,
)
from brain.engineering.generation.models.engineering_generation_request import (
    EngineeringGenerationRequest,
)
from brain.engineering.loop.models.engineering_loop_request import (
    EngineeringLoopRequest,
)
from brain.engineering.testing.models.test_generation_request import (
    TestGenerationRequest,
)
from brain.evolution.evolution_policy import (
    EvolutionPolicy,
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

        task = self._select_task(
            decomposition
        )

        generation_result = (
            self._engineering_generation.generate(
                EngineeringGenerationRequest(
                    task=task,
                    design=design,
                    plan=plan,
                    existing_code=self._existing_code,
                )
            )
        )

        implementation_changes = (
            generation_result.changes
        )

        test_result = self._test_generator.generate(
            TestGenerationRequest(
                task=task,
                design=design,
                plan=plan,
                existing_code=self._existing_code,
                proposed_changes=(
                    implementation_changes
                ),
            )
        )

        proposed_changes = (
            implementation_changes
            + test_result.changes
        )

        if not self._policy.allows_verification(
            mode
        ):
            raise ValueError(
                "evolution mode does not allow "
                "verification"
            )

        loop_request = EngineeringLoopRequest(
            task=task,
            design=design,
            plan=plan,
            existing_code=self._existing_code,
            proposed_changes=proposed_changes,
            verification_command=(
                self._verification_command
            ),
            max_iterations=self._max_iterations,
        )

        engineering_result = (
            self._engineering_loop.execute(
                loop_request
            )
        )

        if (
            mode is EvolutionMode.AUTONOMOUS
            and engineering_result.passed
        ):
            self._integrate(
                integration_request
            )

        return EvolutionResult(
            requested_capability=(
                request.requested_capability
            ),
            requirement=requirement,
            task_decomposition=decomposition,
            design=design,
            plan=plan,
            proposed_changes=proposed_changes,
            engineering_result=engineering_result,
        )

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
            providers=(discovery_request.provider,),
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

    @staticmethod
    def _select_task(
        decomposition,
    ):
        if not decomposition.tasks:
            raise ValueError(
                "task decomposition must contain "
                "at least one task"
            )

        return decomposition.tasks[0]