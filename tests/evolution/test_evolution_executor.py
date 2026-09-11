import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.code.models.code_structure import (
    CodeStructure,
)
from brain.engineering.design.models.system_design import (
    SystemDesign,
)
from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)
from brain.engineering.generation.models.engineering_generation_result import (
    EngineeringGenerationResult,
)
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)
from brain.engineering.requirements.models.requirement import (
    Requirement,
)
from brain.engineering.tasks.models.task import (
    Task,
)
from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)
from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult as GenerationResult,
)
from brain.evolution.evolution_executor import (
    EvolutionExecutor,
)
from brain.evolution.models.evolution_discovery_request import (
    EvolutionDiscoveryRequest,
)
from brain.evolution.models.evolution_proposal import (
    EvolutionProposal,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


class FakeRequirementService:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def understand(self, request):
        self.calls.append(request)
        return self._result


class FakeTaskDecomposer:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def decompose(self, requirement):
        self.calls.append(requirement)
        return self._result


class FakeSystemDesigner:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def design(self, decomposition):
        self.calls.append(decomposition)
        return self._result


class FakePlanner:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def plan(self, decomposition):
        self.calls.append(decomposition)
        return self._result


class FakeEngineeringGeneration:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def generate(self, request):
        self.calls.append(request)
        return self._result


class FakeTestGenerator:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def generate(self, request):
        self.calls.append(request)
        return self._result


class FakeEngineeringLoop:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def execute(self, request):
        self.calls.append(request)
        return self._result


class FakeCapabilityIntegrator:
    def __init__(self):
        self.calls = []

    def integrate(
        self,
        capability,
        verification_passed,
    ):
        self.calls.append(
            (
                capability,
                verification_passed,
            )
        )


class EvolvedCapabilityProvider:
    @staticmethod
    def capability_descriptor():
        return CapabilityDescriptor(
            id="evolved_capability",
            name="Evolved Capability",
            description="A capability created through evolution.",
            version="1.0.0",
            entry_point="brain.evolved.EvolvedCapability",
            dependencies=frozenset(),
        )


class InvalidEvolvedCapabilityProvider:
    pass


class FakeCapabilityDiscovery:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def discover(self, providers):
        self.calls.append(providers)
        return self._result


def _context():
    requirement = Requirement(
        original_request="Add web research.",
        objective="Add web research capability.",
        functional_requirements=frozenset(
            {"web research must work"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Implement web research.",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )

    decomposition = TaskDecomposition(
        requirement=requirement,
        tasks=(task,),
    )

    design = SystemDesign(
        requirement=requirement,
        tasks=(task,),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("implement web research",),
        milestones=("implementation",),
        required_capabilities=frozenset(
            {"web research"}
        ),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=("run tests",),
        confidence=1.0,
    )

    existing_code = CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )

    implementation_change = CodeChange(
        path="brain/research.py",
        operation="create",
        content="research implementation",
    )

    test_change = CodeChange(
        path="tests/test_research.py",
        operation="create",
        content="research test",
    )

    engineering_decision = EngineeringDecision(
        implementation_required=True,
        necessity="required",
        reuse_existing=False,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=("Capability does not exist.",),
    )

    generation_result = EngineeringGenerationResult(
        changes=(implementation_change,),
        engineering_decision=engineering_decision,
        quality_assessment=None,
        optimization_decision=None,
    )

    test_result = GenerationResult(
        changes=(test_change,),
    )

    iteration = EngineeringLoopIteration(
        iteration=1,
        changes=(
            implementation_change,
            test_change,
        ),
        passed=True,
        summary="Verification passed.",
    )

    loop_result = EngineeringLoopResult(
        changes=(
            implementation_change,
            test_change,
        ),
        passed=True,
        iterations=(iteration,),
        termination_reason="verification_passed",
    )

    return (
        requirement,
        task,
        decomposition,
        design,
        plan,
        existing_code,
        generation_result,
        test_result,
        loop_result,
    )


def _executor(
    loop_result=None,
    discovery=None,
    capability_integrator=None,
):
    (
        requirement,
        task,
        decomposition,
        design,
        plan,
        existing_code,
        generation_result,
        test_result,
        default_loop_result,
    ) = _context()

    if loop_result is None:
        loop_result = default_loop_result

    requirement_service = FakeRequirementService(
        requirement
    )

    task_decomposer = FakeTaskDecomposer(
        decomposition
    )

    system_designer = FakeSystemDesigner(
        design
    )

    planner = FakePlanner(plan)

    generation = FakeEngineeringGeneration(
        generation_result
    )

    test_generator = FakeTestGenerator(
        test_result
    )

    engineering_loop = FakeEngineeringLoop(
        loop_result
    )

    executor = EvolutionExecutor(
        requirement_service=requirement_service,
        task_decomposer=task_decomposer,
        system_designer=system_designer,
        planner=planner,
        engineering_generation=generation,
        test_generator=test_generator,
        engineering_loop=engineering_loop,
        existing_code=existing_code,
        verification_command="pytest tests -q",
        max_iterations=3,
        discovery=discovery,
        capability_integrator=capability_integrator,
    )

    return (
        executor,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        generation,
        test_generator,
        engineering_loop,
        (
            requirement,
            task,
            decomposition,
            design,
            plan,
            existing_code,
            generation_result,
            test_result,
            loop_result,
        ),
    )


def test_executor_runs_complete_engineering_pipeline():
    (
        executor,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        generation,
        test_generator,
        engineering_loop,
        context,
    ) = _executor()

    (
        requirement,
        task,
        decomposition,
        design,
        plan,
        existing_code,
        generation_result,
        test_result,
        loop_result,
    ) = context

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert result.requested_capability == (
        "web_research"
    )

    assert result.requirement == requirement
    assert result.task_decomposition == decomposition
    assert result.design == design
    assert result.plan == plan

    assert result.proposed_changes == (
        generation_result.changes
        + test_result.changes
    )

    assert result.engineering_result == (
        loop_result
    )

    assert requirement_service.calls == [
        "Add web research."
    ]

    assert task_decomposer.calls == [
        requirement
    ]

    assert system_designer.calls == [
        decomposition
    ]

    assert planner.calls == [
        decomposition
    ]

    assert len(generation.calls) == 1

    assert generation.calls[0].task == task
    assert generation.calls[0].design == design
    assert generation.calls[0].plan == plan
    assert generation.calls[0].existing_code == (
        existing_code
    )

    assert len(test_generator.calls) == 1

    assert test_generator.calls[0].task == task
    assert test_generator.calls[0].design == design
    assert test_generator.calls[0].plan == plan
    assert test_generator.calls[0].existing_code == (
        existing_code
    )

    assert test_generator.calls[0].proposed_changes == (
        generation_result.changes
    )

    assert len(engineering_loop.calls) == 1

    loop_request = engineering_loop.calls[0]

    assert loop_request.task == task
    assert loop_request.design == design
    assert loop_request.plan == plan
    assert loop_request.existing_code == (
        existing_code
    )

    assert loop_request.proposed_changes == (
        generation_result.changes
        + test_result.changes
    )

    assert loop_request.verification_command == (
        "pytest tests -q"
    )

    assert loop_request.max_iterations == 3


def test_executor_rejects_empty_task_decomposition():
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        context,
    ) = _executor()

    (
        requirement,
        _,
        _,
        design,
        plan,
        existing_code,
        generation_result,
        test_result,
        loop_result,
    ) = context

    empty_decomposition = TaskDecomposition(
        requirement=requirement,
        tasks=(),
    )

    task_decomposer = FakeTaskDecomposer(
        empty_decomposition
    )

    executor = EvolutionExecutor(
        requirement_service=FakeRequirementService(
            requirement
        ),
        task_decomposer=task_decomposer,
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=FakeEngineeringGeneration(
            generation_result
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command="pytest tests -q",
        max_iterations=3,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    with pytest.raises(
        ValueError,
        match="task decomposition must contain",
    ):
        executor.execute(request)


def test_propose_returns_evolution_proposal():
    (
        executor,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        generation,
        test_generator,
        engineering_loop,
        context,
    ) = _executor()

    (
        requirement,
        _,
        decomposition,
        design,
        plan,
        _,
        _,
        _,
        _,
    ) = context

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="proposal",
    )

    result = executor.propose(request)

    assert isinstance(
        result,
        EvolutionProposal,
    )

    assert result.requested_capability == (
        "web_research"
    )

    assert result.requirement == requirement
    assert result.task_decomposition == decomposition
    assert result.design == design
    assert result.plan == plan

    assert requirement_service.calls == [
        "Add web research."
    ]

    assert task_decomposer.calls == [
        requirement
    ]

    assert system_designer.calls == [
        decomposition
    ]

    assert planner.calls == [
        decomposition
    ]

    assert generation.calls == []
    assert test_generator.calls == []
    assert engineering_loop.calls == []


def test_propose_rejects_non_proposal_mode():
    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    with pytest.raises(
        ValueError,
        match="propose\\(\\) requires proposal mode",
    ):
        executor.propose(request)


def test_execute_rejects_proposal_mode():
    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="proposal",
    )

    with pytest.raises(
        ValueError,
        match="proposal mode requires propose",
    ):
        executor.execute(request)


def test_supervised_execution_does_not_integrate():
    integrator = FakeCapabilityIntegrator()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        capability_integrator=integrator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert result.engineering_result.passed
    assert integrator.calls == []


def test_autonomous_execution_requires_discovery_request():
    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    with pytest.raises(
        TypeError,
        match="EvolutionDiscoveryRequest",
    ):
        executor.execute(request)


def test_autonomous_execution_rejects_invalid_discovery_request():
    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    with pytest.raises(
        TypeError,
        match="EvolutionDiscoveryRequest",
    ):
        executor.execute(
            request,
            integration_request=object(),
        )


def test_autonomous_execution_discovers_provider():
    provider = EvolvedCapabilityProvider()

    discovery = FakeCapabilityDiscovery(
        (
            provider.capability_descriptor(),
        )
    )

    integrator = FakeCapabilityIntegrator()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        discovery=discovery,
        capability_integrator=integrator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.engineering_result.passed

    assert discovery.calls == [
        (provider,),
    ]


def test_autonomous_execution_integrates_discovered_capability():
    provider = EvolvedCapabilityProvider()

    capability = provider.capability_descriptor()

    discovery = FakeCapabilityDiscovery(
        (capability,)
    )

    integrator = FakeCapabilityIntegrator()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        discovery=discovery,
        capability_integrator=integrator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.engineering_result.passed

    assert discovery.calls == [
        (provider,),
    ]

    assert integrator.calls == [
        (capability, True),
    ]


def test_autonomous_execution_rejects_provider_without_descriptor():
    provider = InvalidEvolvedCapabilityProvider()

    discovery = FakeCapabilityDiscovery(
        ()
    )

    integrator = FakeCapabilityIntegrator()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        discovery=discovery,
        capability_integrator=integrator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
    )

    with pytest.raises(
        ValueError,
        match="did not expose a capability descriptor",
    ):
        executor.execute(
            request,
            integration_request=discovery_request,
        )

    assert discovery.calls == [
        (provider,),
    ]

    assert integrator.calls == []


def test_autonomous_execution_does_not_integrate_after_failed_verification():
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        context,
    ) = _executor()

    (
        requirement,
        _,
        decomposition,
        design,
        plan,
        existing_code,
        generation_result,
        test_result,
        _,
    ) = context

    failed_loop_result = EngineeringLoopResult(
        changes=(
            generation_result.changes
            + test_result.changes
        ),
        passed=False,
        iterations=(),
        termination_reason="max_iterations_reached",
    )

    provider = EvolvedCapabilityProvider()

    discovery = FakeCapabilityDiscovery(
        (
            provider.capability_descriptor(),
        )
    )

    integrator = FakeCapabilityIntegrator()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor(
        loop_result=failed_loop_result,
        discovery=discovery,
        capability_integrator=integrator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.engineering_result.passed is False
    assert discovery.calls == []
    assert integrator.calls == []