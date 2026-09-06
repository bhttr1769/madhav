from dataclasses import dataclass

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task


@dataclass(frozen=True)
class DebuggingRequest:
    task: Task
    design: SystemDesign
    plan: EngineeringPlan
    existing_code: CodeStructure
    proposed_changes: tuple[CodeChange, ...]
    error_message: str
    traceback: str