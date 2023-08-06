from fastgenomics.process import FGProcess
import pytest


def test_io_throws_on_non_existing_files(app_dir, data_root_none):
    with pytest.raises(FileNotFoundError):
        FGProcess(app_dir, data_root_none)


def test_undefined_for_optional_files(app_dir, data_root):
    fg = FGProcess(app_dir, data_root)
    optional = fg.input["non_existing_optional_input"]
    assert optional.path is None
    assert not optional.exists()
