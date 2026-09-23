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
from brain.evolution.evolution_dependency_planner import (
    EvolutionDependencyPlanner,
)
from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)
from brain.package_managers.models.dependency import (
    Dependency,
)
from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
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
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)
from brain.evolution.evolution_history_builder import (
    EvolutionHistoryBuilder,
)
from brain.evolution.evolution_history_recorder import (
    EvolutionHistoryRecorder,
)
from brain.evolution.evolution_id_generator import (
    EvolutionIdGenerator,
)
from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)
from brain.evolution.models.evolution_checkpoint import (
    EvolutionCheckpoint,
)
from brain.evolution.evolution_checkpoint import (
    EvolutionCheckpointManager,
)
from brain.evolution.models.evolution_dependency_assessment import (
    EvolutionDependencyAssessment,
)
from brain.evolution.models.evolution_dependency_plan import (
    EvolutionDependencyPlan,
)
from brain.evolution.models.evolution_dependency_plan_operation import (
    EvolutionDependencyPlanOperation,
)
from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)
from brain.evolution.models.evolution_dependency_resolution import (
    EvolutionDependencyResolution,
)
from brain.evolution.models.evolution_dependency_resolution_status import (
    EvolutionDependencyResolutionStatus,
)
from brain.evolution.models.evolution_dependency_status import (
    EvolutionDependencyStatus,
)
from brain.package_managers.models.dependency import (
    Dependency,
)


AUTONOMOUS_VERIFICATION_COMMAND = (
    "python",
    "-c",
    "import sys; sys.exit(0)",
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
    def __init__(
        self,
        result,
        exception=None,
        events=None,
    ):
        self._result = result
        self.exception = exception
        self.events = (
            events
            if events is not None
            else []
        )
        self.calls = []

    def execute(self, request):
        self.calls.append(request)

        if self.exception is not None:
            raise self.exception

        self.events.append("engineering")

        return self._result


class FakeCapabilityIntegrator:
    def __init__(
        self,
        events=None,
        exception=None,
    ):
        self.calls = []
        self.events = (
            events
            if events is not None
            else []
        )
        self.exception = exception

    def integrate(
        self,
        capability,
        verification_passed,
    ):
        if self.exception is not None:
            raise self.exception

        self.calls.append(
            (
                capability,
                verification_passed,
            )
        )

        self.events.append("integration")


class FakeCheckpointManager:
    def __init__(
        self,
        events=None,
        has_uncommitted_changes=False,
        has_untracked_files=False,
    ):
        self.calls = []
        self.checkpoints = {}
        self.events = (
            events
            if events is not None
            else []
        )
        self.has_uncommitted_changes = (
            has_uncommitted_changes
        )
        self.has_untracked_files = (
            has_untracked_files
        )

    def create(
        self,
        evolution_id,
        repository_path,
    ):
        self.calls.append(
            (
                "create",
                evolution_id,
                repository_path,
            )
        )

        self.events.append("checkpoint")

        checkpoint = EvolutionCheckpoint(
            evolution_id=evolution_id,
            repository_path=repository_path,
            branch="main",
            commit_hash="base-commit",
            has_uncommitted_changes=(
                self.has_uncommitted_changes
            ),
            has_untracked_files=(
                self.has_untracked_files
            ),
            status=EvolutionCheckpointManager.ACTIVE,
            evolution_commit_hash=None,
        )

        self.checkpoints[evolution_id] = (
            checkpoint
        )

        return checkpoint

    def set_evolution_commit(
        self,
        evolution_id,
        evolution_commit_hash,
    ):
        self.calls.append(
            (
                "set_evolution_commit",
                evolution_id,
                evolution_commit_hash,
            )
        )

        checkpoint = self.checkpoints[
            evolution_id
        ]

        updated = EvolutionCheckpoint(
            evolution_id=checkpoint.evolution_id,
            repository_path=checkpoint.repository_path,
            branch=checkpoint.branch,
            commit_hash=checkpoint.commit_hash,
            has_uncommitted_changes=(
                checkpoint.has_uncommitted_changes
            ),
            has_untracked_files=(
                checkpoint.has_untracked_files
            ),
            status=checkpoint.status,
            evolution_commit_hash=(
                evolution_commit_hash
            ),
        )

        self.checkpoints[evolution_id] = (
            updated
        )

        return updated

    def complete(
        self,
        evolution_id,
    ):
        self.calls.append(
            (
                "complete",
                evolution_id,
            )
        )

        self.events.append("complete")

        checkpoint = self.checkpoints[
            evolution_id
        ]

        updated = EvolutionCheckpoint(
            evolution_id=checkpoint.evolution_id,
            repository_path=checkpoint.repository_path,
            branch=checkpoint.branch,
            commit_hash=checkpoint.commit_hash,
            has_uncommitted_changes=(
                checkpoint.has_uncommitted_changes
            ),
            has_untracked_files=(
                checkpoint.has_untracked_files
            ),
            status=EvolutionCheckpointManager.COMPLETED,
            evolution_commit_hash=(
                checkpoint.evolution_commit_hash
            ),
        )

        self.checkpoints[evolution_id] = (
            updated
        )

        return updated

    def fail(
        self,
        evolution_id,
    ):
        self.calls.append(
            (
                "fail",
                evolution_id,
            )
        )

        self.events.append("fail")

        checkpoint = self.checkpoints[
            evolution_id
        ]

        updated = EvolutionCheckpoint(
            evolution_id=checkpoint.evolution_id,
            repository_path=checkpoint.repository_path,
            branch=checkpoint.branch,
            commit_hash=checkpoint.commit_hash,
            has_uncommitted_changes=(
                checkpoint.has_uncommitted_changes
            ),
            has_untracked_files=(
                checkpoint.has_untracked_files
            ),
            status=EvolutionCheckpointManager.FAILED,
            evolution_commit_hash=(
                checkpoint.evolution_commit_hash
            ),
        )

        self.checkpoints[evolution_id] = (
            updated
        )

        return updated


class FakeEvolutionGitCommit:
    def __init__(
        self,
        events=None,
        exception=None,
    ):
        self.calls = []
        self.events = (
            events
            if events is not None
            else []
        )
        self.exception = exception

    def commit(
        self,
        repository_path,
        paths,
        message,
    ):
        if self.exception is not None:
            raise self.exception

        self.calls.append(
            (
                repository_path,
                paths,
                message,
            )
        )

        self.events.append("commit")

        return "evolution-commit-001"


class FakeIntegrationRecoveryCoordinator:
    def __init__(
        self,
        events=None,
    ):
        self.calls = []
        self.events = (
            events
            if events is not None
            else []
        )

    def recover(
        self,
        checkpoint,
        reason,
    ):
        self.calls.append(
            (
                checkpoint,
                reason,
            )
        )

        self.events.append("recovery")


class FakeEvolutionTaskExecutor:
    def __init__(
        self,
        results_by_task_id,
        exception=None,
        events=None,
    ):
        self._results_by_task_id = (
            results_by_task_id
        )
        self.exception = exception
        self.events = (
            events
            if events is not None
            else []
        )
        self.calls = []
        self.executed_tasks = []

    def execute(
        self,
        task,
        design,
        plan,
        task_id,
    ):
        self.calls.append(
            (
                task,
                design,
                plan,
                task_id,
            )
        )

        if self.exception is not None:
            raise self.exception

        self.executed_tasks.append(
            task_id
        )

        self.events.append("engineering")

        return self._results_by_task_id[
            task_id
        ]


class FakeEvolutionDependencyDiscovery:
    def __init__(self, environment):
        self.environment = environment
        self.calls = []

    def discover(self, signatures):
        self.calls.append(signatures)
        return self.environment


class RecordingEvolutionDependencyPlanner:
    def __init__(self):
        self.delegate = EvolutionDependencyPlanner()
        self.plans = []

    def plan(
        self,
        requirement,
        resolution,
    ):
        plan = self.delegate.plan(
            requirement,
            resolution,
        )

        self.plans.append(plan)

        return plan


class EvolvedCapabilityProvider:
    @staticmethod
    def capability_descriptor():
        return CapabilityDescriptor(
            id="web_research",
            name="Evolved Capability",
            description=(
                "A capability created through evolution."
            ),
            version="1.0.0",
            entry_point=(
                "brain.evolved.EvolvedCapability"
            ),
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


class FakeEvolutionIdGenerator:
    def __init__(self):
        self.calls = 0

    def generate(self):
        self.calls += 1
        return "evo-test-001"


class FakeEvolutionHistoryBuilder:
    def __init__(self):
        self.calls = []

    def build(
        self,
        evolution_id,
        request,
        result,
        started_at,
        completed_at,
        status,
    ):
        self.calls.append(
            (
                evolution_id,
                request,
                result,
                started_at,
                completed_at,
                status,
            )
        )

        return EvolutionHistory(
            evolution_id=evolution_id,
            requested_capability=(
                request.requested_capability
            ),
            objective=request.objective,
            mode=request.mode,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            task_count=len(
                result.task_decomposition.tasks
            ),
            completed_task_count=len(
                result.task_results
            ),
            passed=result.passed,
            termination_reason="test",
        )


class FakeEvolutionHistoryRecorder:
    def __init__(self):
        self.calls = []

    def record(self, history):
        self.calls.append(history)
        

class FakeDependencyDiscovery:
    def __init__(self, environment):
        self._environment = environment
        self.calls = []

    def discover(self, signatures):
        self.calls.append(signatures)
        return self._environment


class FakeDependencyAvailability:
    def __init__(self, assessments):
        self._assessments = assessments
        self.calls = []

    def assess(self, requirement, environment):
        self.calls.append(
            (
                requirement,
                environment,
            )
        )

        return self._assessments[
            requirement.dependency.name
        ]


class FakeDependencyResolution:
    def __init__(self, resolutions):
        self._resolutions = resolutions
        self.calls = []

    def resolve(self, assessment, environment):
        self.calls.append(
            (
                assessment,
                environment,
            )
        )

        return self._resolutions[
            assessment.dependency.name
        ]


class FakeDependencyPlanner:
    def __init__(self, plans):
        self._plans = plans
        self.calls = []

    def plan(self, requirement, resolution):
        self.calls.append(
            (
                requirement,
                resolution,
            )
        )

        return self._plans[
            requirement.dependency.name
        ]

class FakeDependencySafetyPolicy:
    def __init__(
        self,
        allowed,
        reason="Test safety result.",
    ):
        self.allowed = allowed
        self.reason = reason
        self.calls = []

    def evaluate(self, plans):
        self.calls.append(plans)

        from brain.evolution.models.evolution_dependency_safety_result import (
            EvolutionDependencySafetyResult,
        )
        from brain.evolution.models.evolution_dependency_safety_status import (
            EvolutionDependencySafetyStatus,
        )

        return EvolutionDependencySafetyResult(
            status=(
                EvolutionDependencySafetyStatus.ALLOWED
                if self.allowed
                else EvolutionDependencySafetyStatus.BLOCKED
            ),
            reason=self.reason,
        )

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
    requirement_override=None,
    discovery=None,
    capability_integrator=None,
    checkpoint_manager=None,
    evolution_git_commit=None,
    integration_recovery_coordinator=None,
    evolution_id_generator=None,
    checkpoint_uncommitted_changes=False,
    checkpoint_untracked_files=False,
    engineering_loop_exception=None,
    git_commit_exception=None,
    integration_exception=None,
    events=None,
    safety_policy=None,
    verification_command="pytest tests -q",
    dependency_discovery=None,
    dependency_availability=None,
    dependency_resolution=None,
    dependency_planner=None,
    evolution_validator=None,
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
    
    if requirement_override is not None:
        requirement = requirement_override

    if loop_result is None:
        loop_result = default_loop_result

    if events is None:
        events = []

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
        loop_result,
        exception=engineering_loop_exception,
        events=events,
    )

    if checkpoint_manager is None:
        checkpoint_manager = FakeCheckpointManager(
            events=events,
            has_uncommitted_changes=(
                checkpoint_uncommitted_changes
            ),
            has_untracked_files=(
                checkpoint_untracked_files
            ),
        )

    if evolution_git_commit is None:
        evolution_git_commit = FakeEvolutionGitCommit(
            events=events,
            exception=git_commit_exception,
        )

    if integration_recovery_coordinator is None:
        integration_recovery_coordinator = (
            FakeIntegrationRecoveryCoordinator(
                events=events,
            )
        )

    if evolution_id_generator is None:
        evolution_id_generator = (
            FakeEvolutionIdGenerator()
        )

    if capability_integrator is None:
        capability_integrator = FakeCapabilityIntegrator(
            events=events,
            exception=integration_exception,
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
        verification_command=verification_command,
        max_iterations=3,
        discovery=discovery,
        checkpoint_manager=checkpoint_manager,
        evolution_git_commit=evolution_git_commit,
        integration_recovery_coordinator=(
            integration_recovery_coordinator
        ),
        capability_integrator=capability_integrator,
        evolution_id_generator=(
            evolution_id_generator
        ),
        safety_policy=safety_policy,
        dependency_discovery=dependency_discovery,
        dependency_availability=dependency_availability,
        dependency_resolution=dependency_resolution,
        dependency_planner=dependency_planner,
        evolution_validator=evolution_validator,
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


def _task(
    task_id,
    description,
):
    return Task(
        id=task_id,
        description=description,
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )


def _multi_task_decomposition(
    requirement,
    *tasks,
):
    return TaskDecomposition(
        requirement=requirement,
        tasks=tuple(tasks),
    )


def _task_result(
    task_id,
    description,
    passed=True,
):
    change = CodeChange(
        path=f"{task_id}.py",
        operation="create",
        content=f"{task_id} implementation",
    )

    iteration = EngineeringLoopIteration(
        iteration=1,
        changes=(change,),
        passed=passed,
        summary=(
            "Verification passed."
            if passed
            else "Verification failed."
        ),
    )

    loop_result = EngineeringLoopResult(
        changes=(change,),
        passed=passed,
        iterations=(iteration,),
        termination_reason=(
            "verification_passed"
            if passed
            else "max_iterations_reached"
        ),
    )

    return EvolutionTaskResult(
        task_id=task_id,
        task_description=description,
        proposed_changes=(change,),
        engineering_result=loop_result,
    )


def _multi_task_executor(
    task_results,
    verification_command="pytest tests -q",
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
        loop_result,
    ) = _context()

    tasks = tuple(
        _task(
            task_id=task_id,
            description=task_description,
        )
        for task_id, task_description in (
            ("task-1", "First task."),
            ("task-2", "Second task."),
            ("task-3", "Third task."),
        )
        if task_id in task_results
    )

    decomposition = _multi_task_decomposition(
        requirement,
        *tasks,
    )

    task_executor = FakeEvolutionTaskExecutor(
        task_results
    )

    checkpoint_manager = FakeCheckpointManager()

    evolution_git_commit = (
        FakeEvolutionGitCommit()
    )

    integration_recovery_coordinator = (
        FakeIntegrationRecoveryCoordinator()
    )

    capability_integrator = (
        FakeCapabilityIntegrator()
    )

    executor = EvolutionExecutor(
        requirement_service=(
            FakeRequirementService(
                requirement
            )
        ),
        task_decomposer=FakeTaskDecomposer(
            decomposition
        ),
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=(
            FakeEngineeringGeneration(
                generation_result
            )
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command=(
            verification_command
        ),
        max_iterations=3,
        task_executor=task_executor,
        checkpoint_manager=checkpoint_manager,
        evolution_git_commit=(
            evolution_git_commit
        ),
        integration_recovery_coordinator=(
            integration_recovery_coordinator
        ),
        capability_integrator=(
            capability_integrator
        ),
    )

    return (
        executor,
        task_executor,
        checkpoint_manager,
        evolution_git_commit,
        integration_recovery_coordinator,
        capability_integrator,
        requirement,
    )


def _request(
    mode="supervised",
):
    return EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode=mode,
    )

def _dependency():
    return Dependency(
        name="requests",
        version="2.31.0",
        source="requirements.txt",
    )


def _dependency_requirement():
    return EvolutionDependencyRequirement(
        dependency=_dependency(),
        reason="Required by the evolution.",
    )


def _dependency_assessment():
    return EvolutionDependencyAssessment(
        dependency=_dependency(),
        status=EvolutionDependencyStatus.AVAILABLE,
        reason="Dependency is available.",
    )


def _dependency_resolution():
    return EvolutionDependencyResolution(
        assessment=_dependency_assessment(),
        status=(
            EvolutionDependencyResolutionStatus.NOT_REQUIRED
        ),
        package_manager=None,
        reason="No dependency action is required.",
    )


def _dependency_plan(
    operation,
    reason="Test dependency plan.",
):
    return EvolutionDependencyPlan(
        requirement=_dependency_requirement(),
        resolution=_dependency_resolution(),
        operation=operation,
        package_manager=None,
        reason=reason,
    )

def test_proposal_mode_returns_proposal():
    (
        executor,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        _,
        _,
        _,
        context,
    ) = _executor()

    proposal = executor.propose(
        _request(
            mode="proposal",
        )
    )

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

    assert isinstance(
        proposal,
        EvolutionProposal,
    )

    assert (
        proposal.requested_capability
        == "web_research"
    )

    assert proposal.requirement == requirement
    assert proposal.task_decomposition == decomposition
    assert proposal.design == design
    assert proposal.plan == plan

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

    with pytest.raises(
        ValueError,
        match="propose\\(\\) requires proposal mode",
    ):
        executor.propose(
            _request(
                mode="supervised",
            )
        )


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

    with pytest.raises(
        ValueError,
        match=(
            "proposal mode requires propose\\(\\), "
            "not execute\\(\\)"
        ),
    ):
        executor.execute(
            _request(
                mode="proposal",
            )
        )


def test_execute_rejects_non_evolution_request():
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

    with pytest.raises(
        TypeError,
        match="request must be an EvolutionRequest",
    ):
        executor.execute(
            object()
        )


def test_propose_rejects_non_evolution_request():
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

    with pytest.raises(
        TypeError,
        match="request must be an EvolutionRequest",
    ):
        executor.propose(
            object()
        )


def test_supervised_execution_returns_evolution_result():
    (
        executor,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        _,
        _,
        engineering_loop,
        context,
    ) = _executor()

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    (
        requirement,
        task,
        decomposition,
        design,
        plan,
        _,
        _,
        _,
        loop_result,
    ) = context

    assert result.requested_capability == (
        "web_research"
    )

    assert result.requirement == requirement
    assert result.task_decomposition == decomposition
    assert result.design == design
    assert result.plan == plan

    assert result.proposed_changes == (
        CodeChange(
            path="brain/research.py",
            operation="create",
            content="research implementation",
        ),
        CodeChange(
            path="tests/test_research.py",
            operation="create",
            content="research test",
        ),
    )

    assert result.engineering_result == (
        loop_result
    )

    assert len(result.task_results) == 1

    assert result.task_results[0].task_id == (
        task.id
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

    assert len(engineering_loop.calls) == 1


def test_supervised_execution_records_history():
    history_builder = (
        FakeEvolutionHistoryBuilder()
    )

    history_recorder = (
        FakeEvolutionHistoryRecorder()
    )

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
    ) = _context()

    executor = EvolutionExecutor(
        requirement_service=(
            FakeRequirementService(
                requirement
            )
        ),
        task_decomposer=FakeTaskDecomposer(
            decomposition
        ),
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=(
            FakeEngineeringGeneration(
                generation_result
            )
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command=(
            "pytest tests -q"
        ),
        evolution_id_generator=(
            FakeEvolutionIdGenerator()
        ),
        history_builder=history_builder,
        history_recorder=history_recorder,
    )

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    assert len(history_builder.calls) == 1
    assert len(history_recorder.calls) == 1

    history = history_recorder.calls[0]

    assert history.evolution_id == (
        "evo-test-001"
    )

    assert history.requested_capability == (
        "web_research"
    )

    assert history.objective == (
        "Add web research."
    )

    assert history.mode == "supervised"

    assert history.status == "completed"

    assert history.passed is True

    assert result.passed is True


def test_supervised_execution_does_not_create_checkpoint():
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

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    assert result.passed is True


def test_supervised_execution_rejects_integration_request():
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

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        ValueError,
        match=(
            "integration_request is only valid "
            "for autonomous mode"
        ),
    ):
        executor.execute(
            _request(
                mode="supervised",
            ),
            integration_request=discovery_request,
        )


def test_supervised_execution_stops_after_failed_task():
    failed_result = _task_result(
        task_id="task-1",
        description="First task.",
        passed=False,
    )

    successful_result = _task_result(
        task_id="task-2",
        description="Second task.",
        passed=True,
    )

    (
        executor,
        task_executor,
        _,
        _,
        _,
        _,
        _,
    ) = _multi_task_executor(
        {
            "task-1": failed_result,
            "task-2": successful_result,
        }
    )

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    assert task_executor.executed_tasks == [
        "task-1"
    ]

    assert len(result.task_results) == 1

    assert result.passed is False


def test_supervised_execution_runs_all_successful_tasks():
    first_result = _task_result(
        task_id="task-1",
        description="First task.",
        passed=True,
    )

    second_result = _task_result(
        task_id="task-2",
        description="Second task.",
        passed=True,
    )

    third_result = _task_result(
        task_id="task-3",
        description="Third task.",
        passed=True,
    )

    (
        executor,
        task_executor,
        _,
        _,
        _,
        _,
        _,
    ) = _multi_task_executor(
        {
            "task-1": first_result,
            "task-2": second_result,
            "task-3": third_result,
        }
    )

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    assert task_executor.executed_tasks == [
        "task-1",
        "task-2",
        "task-3",
    ]

    assert len(result.task_results) == 3

    assert result.passed is True


def test_supervised_execution_aggregates_changes_from_all_tasks():
    first_result = _task_result(
        task_id="task-1",
        description="First task.",
        passed=True,
    )

    second_result = _task_result(
        task_id="task-2",
        description="Second task.",
        passed=True,
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _multi_task_executor(
        {
            "task-1": first_result,
            "task-2": second_result,
        }
    )

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    assert result.proposed_changes == (
        CodeChange(
            path="task-1.py",
            operation="create",
            content="task-1 implementation",
        ),
        CodeChange(
            path="task-2.py",
            operation="create",
            content="task-2 implementation",
        ),
    )


def test_supervised_execution_records_failed_history():
    failed_result = _task_result(
        task_id="task-1",
        description="First task.",
        passed=False,
    )

    (
        executor,
        _,
        checkpoint_manager,
        _,
        _,
        _,
        _,
    ) = _multi_task_executor(
        {
            "task-1": failed_result,
        }
    )

    result = executor.execute(
        _request(
            mode="supervised",
        )
    )

    assert result.passed is False

    assert checkpoint_manager.calls == []


def test_supervised_execution_raises_when_engineering_fails():
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
        engineering_loop_exception=RuntimeError(
            "engineering failed"
        )
    )

    with pytest.raises(
        RuntimeError,
        match="engineering failed",
    ):
        executor.execute(
            _request(
                mode="supervised",
            )
        )


def test_supervised_execution_rejects_empty_task_decomposition():
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
    ) = _context()

    empty_decomposition = TaskDecomposition(
        requirement=requirement,
        tasks=(),
    )

    executor = EvolutionExecutor(
        requirement_service=(
            FakeRequirementService(
                requirement
            )
        ),
        task_decomposer=FakeTaskDecomposer(
            empty_decomposition
        ),
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=(
            FakeEngineeringGeneration(
                generation_result
            )
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command=(
            "pytest tests -q"
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "task decomposition must contain "
            "at least one task"
        ),
    ):
        executor.execute(
            _request(
                mode="supervised",
            )
        )


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

    with pytest.raises(
        TypeError,
        match=(
            "autonomous execution requires an "
            "EvolutionDiscoveryRequest"
        ),
    ):
        executor.execute(
            _request(
                mode="autonomous",
            )
        )


def test_autonomous_execution_requires_checkpoint_manager():
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
    ) = _context()

    executor = EvolutionExecutor(
        requirement_service=(
            FakeRequirementService(
                requirement
            )
        ),
        task_decomposer=FakeTaskDecomposer(
            decomposition
        ),
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=(
            FakeEngineeringGeneration(
                generation_result
            )
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
        checkpoint_manager=None,
        evolution_git_commit=(
            FakeEvolutionGitCommit()
        ),
        integration_recovery_coordinator=(
            FakeIntegrationRecoveryCoordinator()
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "autonomous execution requires "
            "an EvolutionCheckpointManager"
        ),
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )


def test_autonomous_execution_requires_git_commit():
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
    ) = _context()

    executor = EvolutionExecutor(
        requirement_service=(
            FakeRequirementService(
                requirement
            )
        ),
        task_decomposer=FakeTaskDecomposer(
            decomposition
        ),
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=(
            FakeEngineeringGeneration(
                generation_result
            )
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
        checkpoint_manager=(
            FakeCheckpointManager()
        ),
        evolution_git_commit=None,
        integration_recovery_coordinator=(
            FakeIntegrationRecoveryCoordinator()
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "autonomous execution requires "
            "an EvolutionGitCommit"
        ),
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )


def test_autonomous_execution_requires_integration_recovery_coordinator():
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
    ) = _context()

    executor = EvolutionExecutor(
        requirement_service=(
            FakeRequirementService(
                requirement
            )
        ),
        task_decomposer=FakeTaskDecomposer(
            decomposition
        ),
        system_designer=FakeSystemDesigner(
            design
        ),
        planner=FakePlanner(plan),
        engineering_generation=(
            FakeEngineeringGeneration(
                generation_result
            )
        ),
        test_generator=FakeTestGenerator(
            test_result
        ),
        engineering_loop=FakeEngineeringLoop(
            loop_result
        ),
        existing_code=existing_code,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
        checkpoint_manager=(
            FakeCheckpointManager()
        ),
        evolution_git_commit=(
            FakeEvolutionGitCommit()
        ),
        integration_recovery_coordinator=None,
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "autonomous execution requires "
            "an integration recovery coordinator"
        ),
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )


def test_autonomous_execution_rejects_invalid_integration_request():
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

    with pytest.raises(
        TypeError,
        match=(
            "autonomous execution requires an "
            "EvolutionDiscoveryRequest"
        ),
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=object(),
        )


def test_autonomous_execution_creates_checkpoint_commits_and_completes():
    events = []

    discovery = FakeCapabilityDiscovery(
        (
            EvolvedCapabilityProvider.capability_descriptor(),
        )
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
        _,
    ) = _executor(
        discovery=discovery,
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    request = _request(
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.passed is True

    assert engineering_loop.calls

    assert events == [
        "checkpoint",
        "engineering",
        "commit",
        "integration",
        "complete",
    ]

    assert len(discovery.calls) == 1

    assert len(discovery.calls[0]) == 1

    assert isinstance(
        discovery.calls[0][0],
        EvolvedCapabilityProvider,
    )


def test_autonomous_execution_recovers_when_integration_fails():
    events = []

    discovery = FakeCapabilityDiscovery(
        (
            EvolvedCapabilityProvider.capability_descriptor(),
        )
    )

    recovery = (
        FakeIntegrationRecoveryCoordinator(
            events=events
        )
    )

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
        integration_recovery_coordinator=(
            recovery
        ),
        integration_exception=RuntimeError(
            "integration failed"
        ),
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    request = _request(
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match="integration failed",
    ):
        executor.execute(
            request,
            integration_request=discovery_request,
        )

    assert len(recovery.calls) == 1

    checkpoint = recovery.calls[0][0]

    assert checkpoint.evolution_commit_hash == (
        "evolution-commit-001"
    )

    assert checkpoint.status == (
        EvolutionCheckpointManager.ACTIVE
    )


def test_autonomous_execution_rejects_unsafe_repository_before_engineering():
    events = []

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
        _,
    ) = _executor(
        checkpoint_uncommitted_changes=True,
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )

    assert engineering_loop.calls == []

    assert events == [
        "checkpoint",
        "fail",
    ]


def test_autonomous_execution_rejects_untracked_repository_before_engineering():
    events = []

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
        _,
    ) = _executor(
        checkpoint_untracked_files=True,
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )

    assert engineering_loop.calls == []

    assert events == [
        "checkpoint",
        "fail",
    ]


def test_autonomous_execution_recovers_after_engineering_failure():
    events = []

    recovery = (
        FakeIntegrationRecoveryCoordinator(
            events=events
        )
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
        _,
    ) = _executor(
        integration_recovery_coordinator=(
            recovery
        ),
        engineering_loop_exception=RuntimeError(
            "engineering failed"
        ),
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match="engineering failed",
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )

    assert len(recovery.calls) == 0

    assert events == [
        "checkpoint",
        "fail",
    ]


def test_autonomous_execution_does_not_commit_after_failed_verification():
    events = []

    failed_result = _task_result(
        task_id="task-1",
        description="First task.",
        passed=False,
    )

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
        loop_result=failed_result.engineering_result,
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        _request(
            mode="autonomous",
        ),
        integration_request=discovery_request,
    )

    assert result.passed is False

    assert "commit" not in events

    assert "integration" not in events


def test_autonomous_execution_does_not_integrate_after_commit_failure():
    events = []

    discovery = FakeCapabilityDiscovery(
        (
            EvolvedCapabilityProvider.capability_descriptor(),
        )
    )

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
        git_commit_exception=RuntimeError(
            "commit failed"
        ),
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match="commit failed",
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )

    assert "integration" not in events


def test_autonomous_execution_orders_successful_lifecycle():
    events = []

    discovery = FakeCapabilityDiscovery(
        (
            EvolvedCapabilityProvider.capability_descriptor(),
        )
    )

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
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    executor.execute(
        _request(
            mode="autonomous",
        ),
        integration_request=discovery_request,
    )

    assert events == [
        "checkpoint",
        "engineering",
        "commit",
        "integration",
        "complete",
    ]


def test_autonomous_execution_passes_committed_checkpoint_to_recovery():
    events = []

    discovery = FakeCapabilityDiscovery(
        (
            EvolvedCapabilityProvider.capability_descriptor(),
        )
    )

    recovery = (
        FakeIntegrationRecoveryCoordinator(
            events=events
        )
    )

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
        integration_recovery_coordinator=(
            recovery
        ),
        integration_exception=RuntimeError(
            "integration failed"
        ),
        events=events,
        verification_command=(
            AUTONOMOUS_VERIFICATION_COMMAND
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match="integration failed",
    ):
        executor.execute(
            _request(
                mode="autonomous",
            ),
            integration_request=discovery_request,
        )

    assert len(recovery.calls) == 1

    checkpoint = recovery.calls[0][0]

    assert checkpoint.evolution_commit_hash == (
        "evolution-commit-001"
    )

    assert checkpoint.status == (
        EvolutionCheckpointManager.ACTIVE
    )


def _dependency_requirement(
    name="requests",
    version="2.31.0",
):
    dependency = Dependency(
        name=name,
        version=version,
        source="requirements.txt",
    )

    return EvolutionDependencyRequirement(
        dependency=dependency,
        reason=(
            "The evolution implementation "
            "requires the package."
        ),
    )


def _dependency_environment(
    dependencies=(),
    managers=(),
):
    return PackageManagerEnvironment(
        managers=set(managers),
        dependency_files=set(),
        dependencies=set(dependencies),
        lifecycles=set(),
    )


def _request_with_dependencies(
    requirements,
):
    return EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
        dependency_requirements=tuple(
            requirements
        ),
    )


def test_executor_dependency_gate_is_unchanged_when_no_dependencies_exist():
    dependency_discovery = (
        FakeEvolutionDependencyDiscovery(
            _dependency_environment()
        )
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        dependency_discovery=dependency_discovery,
    )

    result = executor.execute(
        _request_with_dependencies(())
    )

    assert result.passed is True

    assert dependency_discovery.calls == []

    assert len(engineering_loop.calls) == 1


def test_executor_allows_engineering_when_dependency_is_available():
    requirement = _dependency_requirement()

    dependency = requirement.dependency

    dependency_discovery = (
        FakeEvolutionDependencyDiscovery(
            _dependency_environment(
                dependencies=(dependency,),
            )
        )
    )

    planner = (
        RecordingEvolutionDependencyPlanner()
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        dependency_discovery=dependency_discovery,
        dependency_planner=planner,
    )

    result = executor.execute(
        _request_with_dependencies(
            (requirement,)
        ),
        dependency_signatures=(
            "requirements.txt",
        ),
    )

    assert result.passed is True

    assert dependency_discovery.calls == [
        ("requirements.txt",),
    ]

    assert (
        planner.plans[0].operation.value
        == "no_action"
    )

    assert len(engineering_loop.calls) == 1


def test_executor_blocks_engineering_when_missing_dependency_is_resolvable():
    requirement = _dependency_requirement()

    dependency_discovery = (
        FakeEvolutionDependencyDiscovery(
            _dependency_environment(
                managers=(
                    type(
                        "Manager",
                        (),
                        {"name": "pip"},
                    )(),
                ),
            )
        )
    )

    planner = (
        RecordingEvolutionDependencyPlanner()
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        dependency_discovery=dependency_discovery,
        dependency_planner=planner,
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "dependency safety validation failed: "
            "dependency addition requires explicit "
            "dependency mutation authorization"
        ),
    ):
        executor.execute(
            _request_with_dependencies(
                (requirement,)
            ),
            dependency_signatures=(
                "requirements.txt",
            ),
        )

    assert (
        planner.plans[0].operation.value
        == "add"
    )

    assert engineering_loop.calls == []


def test_executor_blocks_engineering_when_dependency_version_mismatch_is_resolvable():
    requirement = _dependency_requirement(
        version="2.32.0",
    )

    installed = Dependency(
        name="requests",
        version="2.31.0",
        source="requirements.txt",
    )

    dependency_discovery = (
        FakeEvolutionDependencyDiscovery(
            _dependency_environment(
                dependencies=(installed,),
                managers=(
                    type(
                        "Manager",
                        (),
                        {"name": "pip"},
                    )(),
                ),
            )
        )
    )

    planner = (
        RecordingEvolutionDependencyPlanner()
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        dependency_discovery=dependency_discovery,
        dependency_planner=planner,
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "dependency safety validation failed: "
            "dependency update requires explicit "
            "dependency mutation authorization"
        ),
    ):
        executor.execute(
            _request_with_dependencies(
                (requirement,)
            ),
            dependency_signatures=(
                "requirements.txt",
            ),
        )

    assert (
        planner.plans[0].operation.value
        == "update"
    )

    assert engineering_loop.calls == []


def test_executor_blocks_engineering_when_dependency_is_not_resolvable():
    requirement = _dependency_requirement()

    dependency_discovery = (
        FakeEvolutionDependencyDiscovery(
            _dependency_environment()
        )
    )

    planner = (
        RecordingEvolutionDependencyPlanner()
    )

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        dependency_discovery=dependency_discovery,
        dependency_planner=planner,
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "dependency safety validation failed: "
            "dependency plan is blocked:"
        ),
    ):
        executor.execute(
            _request_with_dependencies(
                (requirement,)
            ),
            dependency_signatures=(
                "requirements.txt",
            ),
        )

    assert (
        planner.plans[0].operation.value
        == "blocked"
    )

    assert engineering_loop.calls == []


def test_autonomous_dependency_block_marks_checkpoint_failed_and_skips_engineering():
    requirement = _dependency_requirement()

    dependency_discovery = (
        FakeEvolutionDependencyDiscovery(
            _dependency_environment()
        )
    )

    planner = (
        RecordingEvolutionDependencyPlanner()
    )

    events = []

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        dependency_discovery=dependency_discovery,
        dependency_planner=planner,
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
        dependency_requirements=(
            requirement,
        ),
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "dependency safety validation failed: "
            "dependency plan is blocked:"
        ),
    ):
        executor.execute(
            request,
            integration_request=(
                discovery_request
            ),
            dependency_signatures=(
                "requirements.txt",
            ),
        )

    assert engineering_loop.calls == []

    assert "commit" not in events

    assert "integration" not in events

    assert "fail" in events
    
def test_executor_allows_evolution_when_dependency_requires_no_action():
    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor()

    dependency_plan = _dependency_plan(
        EvolutionDependencyPlanOperation.NO_ACTION,
    )

    safety_policy = FakeDependencySafetyPolicy(
        allowed=True,
    )

    executor._dependency_safety_policy = safety_policy

    result = executor._validate_dependency_safety(
        plans=(dependency_plan,),
        evolution_id="evolution-1",
        checkpoint=None,
    )

    assert result.allowed is True
    
def test_executor_blocks_dependency_add_before_engineering():
    events = []

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        events=events,
    )

    executor._dependency_safety_policy = (
        FakeDependencySafetyPolicy(
            allowed=False,
            reason=(
                "dependency addition requires "
                "explicit dependency mutation authorization"
            ),
        )
    )

    dependency_plan = _dependency_plan(
        EvolutionDependencyPlanOperation.ADD,
    )

    with pytest.raises(
        RuntimeError,
        match="dependency safety validation failed",
    ):
        executor._validate_dependency_safety(
            plans=(dependency_plan,),
            evolution_id="evolution-1",
            checkpoint=None,
        )

    assert engineering_loop.calls == []
    assert "engineering" not in events
    
def test_executor_blocks_dependency_update_before_engineering():
    events = []

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        engineering_loop,
        _,
    ) = _executor(
        events=events,
    )

    executor._dependency_safety_policy = (
        FakeDependencySafetyPolicy(
            allowed=False,
            reason=(
                "dependency update requires "
                "explicit dependency mutation authorization"
            ),
        )
    )

    dependency_plan = _dependency_plan(
        EvolutionDependencyPlanOperation.UPDATE,
    )

    with pytest.raises(
        RuntimeError,
        match="dependency safety validation failed",
    ):
        executor._validate_dependency_safety(
            plans=(dependency_plan,),
            evolution_id="evolution-1",
            checkpoint=None,
        )

    assert engineering_loop.calls == []
    assert "engineering" not in events