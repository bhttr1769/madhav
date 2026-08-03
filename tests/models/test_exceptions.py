import pytest

from brain.exceptions.errors import UnsupportedFileTypeError
from brain.manager import BrainManager
from brain.factories.brain_factory import BrainFactory
from tests.utils.testing_factory import TestBrainFactory

def test_unsupported_file_type():

    manager = TestBrainFactory.create()

    with pytest.raises(UnsupportedFileTypeError):
        manager.read("sample.xyz")