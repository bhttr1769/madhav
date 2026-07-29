import pytest

from brain.exceptions.errors import UnsupportedFileTypeError
from brain.manager import BrainManager
from brain.factories.brain_factory import BrainFactory


def test_unsupported_file_type():

    manager = BrainFactory.create()

    with pytest.raises(UnsupportedFileTypeError):
        manager.read("sample.xyz")