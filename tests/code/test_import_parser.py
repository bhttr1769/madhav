from brain.code.models.import_model import (
    ImportModel,
)

from brain.code.parsing.import_parser import (
    ImportParser,
)


SOURCE = """
import os
import numpy as np
from pathlib import Path
from collections import defaultdict as dd
from package.submodule import thing
"""


def test_import_parser_extracts_imports():

    imports = ImportParser().parse(
        SOURCE,
        "example.py",
    )

    assert imports == frozenset({
        ImportModel(
            module="os",
            name=None,
            alias=None,
            path="example.py",
        ),
        ImportModel(
            module="numpy",
            name=None,
            alias="np",
            path="example.py",
        ),
        ImportModel(
            module="pathlib",
            name="Path",
            alias=None,
            path="example.py",
        ),
        ImportModel(
            module="collections",
            name="defaultdict",
            alias="dd",
            path="example.py",
        ),
        ImportModel(
            module="package.submodule",
            name="thing",
            alias=None,
            path="example.py",
        ),
    })


def test_import_parser_handles_multiple_names():

    source = """
from os import path, environ
"""

    imports = ImportParser().parse(
        source,
        "example.py",
    )

    assert imports == frozenset({
        ImportModel(
            module="os",
            name="path",
            alias=None,
            path="example.py",
        ),
        ImportModel(
            module="os",
            name="environ",
            alias=None,
            path="example.py",
        ),
    })


def test_import_parser_handles_relative_import():

    source = """
from .utils import helper
"""

    imports = ImportParser().parse(
        source,
        "example.py",
    )

    assert imports == frozenset({
        ImportModel(
            module="utils",
            name="helper",
            alias=None,
            level=1,
            path="example.py",
        ),
    })


def test_import_parser_records_source_path():

    parser = ImportParser()

    imports = parser.parse(
        "import brain.safety",
        path="brain/code/example.py",
    )

    import_model = next(
        iter(imports)
    )

    assert (
        import_model.path
        == "brain/code/example.py"
    )


def test_import_parser_returns_empty_for_no_imports():

    imports = ImportParser().parse(
        """
def hello():
    pass
""",
        "example.py",
    )

    assert imports == frozenset()