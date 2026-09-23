from enum import Enum


class EvolutionImprovementCategory(
    Enum,
):
    """
    Represents the category of an identified
    evolution-engine improvement opportunity.
    """

    REQUIREMENT_UNDERSTANDING = (
        "requirement_understanding"
    )

    TASK_DECOMPOSITION = (
        "task_decomposition"
    )

    SYSTEM_DESIGN = (
        "system_design"
    )

    ENGINEERING_PLANNING = (
        "engineering_planning"
    )

    CODE_GENERATION = (
        "code_generation"
    )

    TEST_GENERATION = (
        "test_generation"
    )

    VERIFICATION = (
        "verification"
    )

    DEBUGGING = (
        "debugging"
    )

    REFACTORING = (
        "refactoring"
    )

    CAPABILITY_DISCOVERY = (
        "capability_discovery"
    )

    CAPABILITY_INTEGRATION = (
        "capability_integration"
    )

    DEPENDENCY_MANAGEMENT = (
        "dependency_management"
    )

    SAFETY = (
        "safety"
    )

    RECOVERY = (
        "recovery"
    )

    ORCHESTRATION = (
        "orchestration"
    )