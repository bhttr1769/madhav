from dataclasses import dataclass

from brain.code.models.call_model import (
    CallModel,
)

from brain.code.models.class_model import (
    ClassModel,
)

from brain.code.models.function_model import (
    FunctionModel,
)

from brain.code.models.import_model import (
    ImportModel,
)

from brain.code.models.module import (
    Module,
)


@dataclass(frozen=True)
class CodeStructure:
    """
    Represents the complete structural understanding
    of a Python codebase.
    """

    modules: frozenset[Module]

    classes: frozenset[ClassModel]

    functions: frozenset[FunctionModel]

    imports: frozenset[ImportModel]

    calls: frozenset[CallModel]