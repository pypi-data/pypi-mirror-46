import pytest
from pathlib import Path
from fastgenomics.process import FGProcess
from fastgenomics.testing import cleanoutput

HERE = Path(__file__).parent
DATA = HERE / "data"
APPS = HERE / "apps"



@pytest.fixture
def app_dir():
    return APPS / "working"


@pytest.fixture
def app_dir_validation_error():
    return APPS / "validation_error"


@pytest.fixture
def app_dir_missing_files():
    return APPS / "missing_files"


@pytest.fixture
def app_dir_non_existing():
    path = APPS / "non_existing"
    assert not path.exists()
    return path


@pytest.fixture
def app_dir_runtime_error():
    return APPS / "runtime_error"


@pytest.fixture
def data_root():
    return DATA / "working_1"


@pytest.fixture
def data_root_colnames():
    return DATA / "working_1_colnames"


@pytest.fixture
def data_root_2():
    return DATA / "working_2"


@pytest.fixture
def data_root_none():
    return DATA / "non_existing"


@pytest.fixture
def data_root_missing_files():
    return DATA / "missing_files"


@pytest.fixture
def data_root_no_mapping_file():
    return DATA / "no_mapping_file"


@pytest.fixture(params=["working_1", "working_3"])
def fgprocess(request, app_dir):
    fg = FGProcess(app_dir, DATA / request.param)
    cleanoutput(fg)
    return fg


@pytest.mark.anndata
@pytest.fixture
def adata(fgprocess):
    import fastgenomics.external.anndata as fgad

    return fgad.read(
        expr=fgprocess.input["some_input"],
        gene_meta=fgprocess.input["genes"],
        cell_meta=fgprocess.input["cells"],
    )


# data-specific fixtures for test_external
@pytest.fixture
def fgprocess_1(app_dir, data_root):
    fg = FGProcess(app_dir, data_root)
    cleanoutput(fg)
    return fg


@pytest.fixture
def fgprocess_anndata(app_dir, data_root):
    fg = FGProcess(app_dir, data_root)
    cleanoutput(fg)
    return fg


# data-specific fixtures for test_external
@pytest.fixture
def fgprocess_1_colnames(app_dir, data_root_colnames):
    fg = FGProcess(app_dir, data_root_colnames)
    cleanoutput(fg)
    return fg


@pytest.fixture
def summary(fgprocess_1):
    fgprocess_1.summary.template = fgprocess_1.app.app_dir / "summary.md.j2"
    return fgprocess_1.summary


@pytest.mark.anndata
@pytest.fixture
def adata_1(fgprocess_1):
    import fastgenomics.external.anndata as fgad

    return fgad.read(
        expr=fgprocess_1.input["some_input"],
        gene_meta=fgprocess_1.input["genes"],
        cell_meta=fgprocess_1.input["cells"],
    )

@pytest.fixture
def anndata_app_dir():
    return APPS / "working_anndata"

@pytest.fixture
def anndata_data_root():
    return DATA / "working_anndata"


@pytest.fixture
def anndata_tmf_data_root():
    return DATA / "anndata_too_many_files"


@pytest.fixture
def anndata_tmf_app_dir():
    return APPS / "anndata_too_many_files"


@pytest.fixture
def fgprocess_anndata_tmf(anndata_tmf_app_dir, anndata_tmf_data_root):
    fg = FGProcess(anndata_tmf_app_dir, anndata_tmf_data_root)
    cleanoutput(fg)
    return fg


@pytest.fixture
def anndata_wt_data_root():
    return DATA / "anndata_wrong_type"


@pytest.fixture
def anndata_wt_app_dir():
    return APPS / "anndata_wrong_type"


@pytest.fixture
def fgprocess_anndata_wt(anndata_wt_app_dir, anndata_wt_data_root):
    fg = FGProcess(anndata_wt_app_dir, anndata_wt_data_root)
    cleanoutput(fg)
    return fg    
