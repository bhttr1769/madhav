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


class EvolvedCapabilityProvider:
    @staticmethod
    def capability_descriptor():
        return CapabilityDescriptor(
            id="evolved_capability",
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
                result.requested_capability
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
        verification_command="pytest tests -q",
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

    evolution_id_generator = (
        FakeEvolutionIdGenerator()
    )

    executor = EvolutionExecutor(
        requirement_service=FakeRequirementService(
            requirement
        ),
        task_decomposer=FakeTaskDecomposer(
            decomposition
        ),
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
        task_executor=task_executor,
        checkpoint_manager=checkpoint_manager,
        evolution_git_commit=evolution_git_commit,
        integration_recovery_coordinator=(
            integration_recovery_coordinator
        ),
        evolution_id_generator=(
            evolution_id_generator
        ),
    )

    return (
        executor,
        task_executor,
        requirement,
        decomposition,
        design,
        plan,
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
        repository_path="D:/Madhav",
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
        repository_path="D:/Madhav",
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
        repository_path="D:/Madhav",
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
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.engineering_result.passed is False
    assert discovery.calls == []
    assert integrator.calls == []


def test_executor_executes_all_tasks_in_sequence():
    task_results = {
        "task-1": _task_result(
            "task-1",
            "First task.",
        ),
        "task-2": _task_result(
            "task-2",
            "Second task.",
        ),
    }

    executor, task_executor, _, _, _, _ = (
        _multi_task_executor(
            task_results
        )
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert task_executor.executed_tasks == [
        "task-1",
        "task-2",
    ]

    assert [
        task_result.task_id
        for task_result in result.task_results
    ] == [
        "task-1",
        "task-2",
    ]


def test_executor_aggregates_changes_from_all_tasks():
    task_results = {
        "task-1": _task_result(
            "task-1",
            "First task.",
        ),
        "task-2": _task_result(
            "task-2",
            "Second task.",
        ),
    }

    executor, _, _, _, _, _ = (
        _multi_task_executor(
            task_results
        )
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    expected_changes = (
        task_results["task-1"].proposed_changes
        + task_results["task-2"].proposed_changes
    )

    assert result.all_proposed_changes == (
        expected_changes
    )


def test_executor_stops_after_first_failed_task():
    task_results = {
        "task-1": _task_result(
            "task-1",
            "First task.",
            passed=False,
        ),
        "task-2": _task_result(
            "task-2",
            "Second task.",
            passed=True,
        ),
    }

    executor, task_executor, _, _, _, _ = (
        _multi_task_executor(
            task_results
        )
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert task_executor.executed_tasks == [
        "task-1",
    ]

    assert len(result.task_results) == 1
    assert result.passed is False


def test_executor_passes_when_all_tasks_pass():
    task_results = {
        "task-1": _task_result(
            "task-1",
            "First task.",
        ),
        "task-2": _task_result(
            "task-2",
            "Second task.",
        ),
    }

    executor, task_executor, _, _, _, _ = (
        _multi_task_executor(
            task_results
        )
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert task_executor.executed_tasks == [
        "task-1",
        "task-2",
    ]

    assert len(result.task_results) == 2
    assert result.passed is True


def test_autonomous_execution_integrates_only_after_all_tasks_pass():
    task_results = {
        "task-1": _task_result(
            "task-1",
            "First task.",
        ),
        "task-2": _task_result(
            "task-2",
            "Second task.",
        ),
    }

    (
        executor,
        task_executor,
        requirement,
        decomposition,
        design,
        plan,
    ) = _multi_task_executor(
        task_results
    )

    provider = EvolvedCapabilityProvider()

    capability = provider.capability_descriptor()

    discovery = FakeCapabilityDiscovery(
        (capability,)
    )

    integrator = FakeCapabilityIntegrator()

    executor._discovery = discovery
    executor._capability_integrator = integrator

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.passed is True

    assert task_executor.executed_tasks == [
        "task-1",
        "task-2",
    ]

    assert discovery.calls == [
        (provider,),
    ]

    assert integrator.calls == [
        (capability, True),
    ]


def test_autonomous_execution_does_not_integrate_after_multi_task_failure():
    task_results = {
        "task-1": _task_result(
            "task-1",
            "First task.",
            passed=True,
        ),
        "task-2": _task_result(
            "task-2",
            "Second task.",
            passed=False,
        ),
        "task-3": _task_result(
            "task-3",
            "Third task.",
            passed=True,
        ),
    }

    (
        executor,
        task_executor,
        _,
        _,
        _,
        _,
    ) = _multi_task_executor(
        task_results
    )

    provider = EvolvedCapabilityProvider()

    capability = provider.capability_descriptor()

    discovery = FakeCapabilityDiscovery(
        (capability,)
    )

    integrator = FakeCapabilityIntegrator()

    executor._discovery = discovery
    executor._capability_integrator = integrator

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.passed is False

    assert task_executor.executed_tasks == [
        "task-1",
        "task-2",
    ]

    assert discovery.calls == []
    assert integrator.calls == []


def test_executor_records_evolution_history():
    history_recorder = (
        FakeEvolutionHistoryRecorder()
    )

    history_builder = (
        FakeEvolutionHistoryBuilder()
    )

    id_generator = (
        FakeEvolutionIdGenerator()
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
        evolution_id_generator=id_generator,
    )

    executor._history_recorder = (
        history_recorder
    )

    executor._history_builder = (
        history_builder
    )

    executor._evolution_id_generator = (
        id_generator
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert id_generator.calls == 1

    assert len(
        history_builder.calls
    ) == 1

    (
        evolution_id,
        recorded_request,
        recorded_result,
        started_at,
        completed_at,
        status,
    ) = history_builder.calls[0]

    assert evolution_id == (
        "evo-test-001"
    )

    assert recorded_request == request
    assert recorded_result == result

    assert started_at <= completed_at
    assert status == "completed"

    assert len(
        history_recorder.calls
    ) == 1

    history = history_recorder.calls[0]

    assert isinstance(
        history,
        EvolutionHistory,
    )

    assert history.evolution_id == (
        "evo-test-001"
    )


def test_executor_records_failed_evolution():
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
        termination_reason=(
            "max_iterations_reached"
        ),
    )

    history_recorder = (
        FakeEvolutionHistoryRecorder()
    )

    history_builder = (
        FakeEvolutionHistoryBuilder()
    )

    id_generator = (
        FakeEvolutionIdGenerator()
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
        loop_result=failed_loop_result,
        evolution_id_generator=id_generator,
    )

    executor._history_recorder = (
        history_recorder
    )

    executor._history_builder = (
        history_builder
    )

    executor._evolution_id_generator = (
        id_generator
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="supervised",
    )

    result = executor.execute(request)

    assert result.passed is False

    assert len(
        history_builder.calls
    ) == 1

    assert (
        history_builder.calls[0][-1]
        == "failed"
    )

    assert len(
        history_recorder.calls
    ) == 1

    assert (
        history_recorder.calls[0].passed
        is False
    )


def test_proposal_mode_does_not_record_history():
    history_recorder = (
        FakeEvolutionHistoryRecorder()
    )

    history_builder = (
        FakeEvolutionHistoryBuilder()
    )

    id_generator = (
        FakeEvolutionIdGenerator()
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
        evolution_id_generator=id_generator,
    )

    executor._history_recorder = (
        history_recorder
    )

    executor._history_builder = (
        history_builder
    )

    executor._evolution_id_generator = (
        id_generator
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="proposal",
    )

    result = executor.propose(request)

    assert result.requested_capability == (
        "web_research"
    )

    assert id_generator.calls == 0
    assert history_builder.calls == []
    assert history_recorder.calls == []


def test_autonomous_execution_creates_checkpoint_commits_and_completes():
    provider = EvolvedCapabilityProvider()

    capability = provider.capability_descriptor()

    discovery = FakeCapabilityDiscovery(
        (capability,)
    )

    integrator = FakeCapabilityIntegrator()
    checkpoint_manager = FakeCheckpointManager()
    git_commit = FakeEvolutionGitCommit()
    recovery = FakeIntegrationRecoveryCoordinator()
    id_generator = FakeEvolutionIdGenerator()

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
        checkpoint_manager=checkpoint_manager,
        evolution_git_commit=git_commit,
        integration_recovery_coordinator=recovery,
        evolution_id_generator=id_generator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.passed is True

    assert checkpoint_manager.calls == [
        (
            "create",
            "evo-test-001",
            "D:/Madhav",
        ),
        (
            "set_evolution_commit",
            "evo-test-001",
            "evolution-commit-001",
        ),
        (
            "complete",
            "evo-test-001",
        ),
    ]

    assert git_commit.calls == [
        (
            "D:/Madhav",
            (
                "brain/research.py",
                "tests/test_research.py",
            ),
            "evolution: web_research",
        ),
    ]

    assert integrator.calls == [
        (capability, True),
    ]

    assert recovery.calls == []


def test_autonomous_execution_recovers_when_integration_fails():
    provider = EvolvedCapabilityProvider()

    discovery = FakeCapabilityDiscovery(
        (
            provider.capability_descriptor(),
        )
    )

    checkpoint_manager = FakeCheckpointManager()
    git_commit = FakeEvolutionGitCommit()
    recovery = FakeIntegrationRecoveryCoordinator()
    id_generator = FakeEvolutionIdGenerator()

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
        capability_integrator=FakeCapabilityIntegrator(
            exception=RuntimeError(
                "integration failed"
            )
        ),
        checkpoint_manager=checkpoint_manager,
        evolution_git_commit=git_commit,
        integration_recovery_coordinator=recovery,
        evolution_id_generator=id_generator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
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

    assert checkpoint_manager.calls == [
        (
            "create",
            "evo-test-001",
            "D:/Madhav",
        ),
        (
            "set_evolution_commit",
            "evo-test-001",
            "evolution-commit-001",
        ),
        (
            "fail",
            "evo-test-001",
        ),
    ]

    assert recovery.calls

    assert recovery.calls[0][1] == (
        "integration failed"
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
        _,
        _,
        _,
    ) = _executor(
        checkpoint_uncommitted_changes=True,
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match="uncommitted changes",
    ):
        executor.execute(
            request,
            integration_request=discovery_request,
        )

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
        _,
        _,
        _,
    ) = _executor(
        checkpoint_untracked_files=True,
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=EvolvedCapabilityProvider(),
        repository_path="D:/Madhav",
    )

    with pytest.raises(
        RuntimeError,
        match="untracked files",
    ):
        executor.execute(
            request,
            integration_request=discovery_request,
        )

    assert events == [
        "checkpoint",
        "fail",
    ]


def test_autonomous_execution_recovers_after_engineering_failure():
    events = []

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
        ),
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
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
            request,
            integration_request=discovery_request,
        )

    assert events == [
        "checkpoint",
        "fail",
    ]


def test_autonomous_execution_does_not_commit_after_failed_verification():
    events = []

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
        _,
        _,
        _,
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
        termination_reason=(
            "max_iterations_reached"
        ),
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
        loop_result=failed_loop_result,
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
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

    assert result.passed is False
    assert "commit" not in events
    assert "integration" not in events


def test_autonomous_execution_does_not_integrate_after_commit_failure():
    events = []

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
        git_commit_exception=RuntimeError(
            "commit failed"
        ),
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
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
            request,
            integration_request=discovery_request,
        )

    assert "integration" not in events


def test_autonomous_execution_orders_successful_lifecycle():
    events = []

    provider = EvolvedCapabilityProvider()

    discovery = FakeCapabilityDiscovery(
        (
            provider.capability_descriptor(),
        )
    )

    integrator = FakeCapabilityIntegrator(
        events=events,
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
        capability_integrator=integrator,
        events=events,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
        repository_path="D:/Madhav",
    )

    result = executor.execute(
        request,
        integration_request=discovery_request,
    )

    assert result.passed is True

    assert events == [
        "checkpoint",
        "engineering",
        "commit",
        "integration",
        "complete",
    ]


def test_autonomous_execution_passes_committed_checkpoint_to_recovery():
    provider = EvolvedCapabilityProvider()

    discovery = FakeCapabilityDiscovery(
        (
            provider.capability_descriptor(),
        )
    )

    integrator = FakeCapabilityIntegrator(
        exception=RuntimeError(
            "integration failed"
        ),
    )

    checkpoint_manager = FakeCheckpointManager()
    git_commit = FakeEvolutionGitCommit()
    recovery = FakeIntegrationRecoveryCoordinator()
    id_generator = FakeEvolutionIdGenerator()

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
        checkpoint_manager=checkpoint_manager,
        evolution_git_commit=git_commit,
        integration_recovery_coordinator=recovery,
        evolution_id_generator=id_generator,
    )

    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="autonomous",
    )

    discovery_request = EvolutionDiscoveryRequest(
        provider=provider,
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