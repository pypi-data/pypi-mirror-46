from fastgenomics.defaults import DEFAULT_APP_DIR, DEFAULT_DATA_ROOT, INPUT_FILE_MAPPING
from fastgenomics.process import FGProcess
import pytest
from pathlib import Path


def test_values():
    assert DEFAULT_APP_DIR == Path("tests/apps/working")
    assert DEFAULT_DATA_ROOT == Path("tests/data/working_1_no_mapping")
    assert "some_input" in INPUT_FILE_MAPPING


def test_process():
    FGProcess()


def test_process_raises():
    with pytest.raises(RuntimeError):
        FGProcess(data_dir="tests/data/working_1")
