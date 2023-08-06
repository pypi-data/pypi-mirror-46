from fastgenomics.process import FGProcess
import fastgenomics.external.anndata as fgad
import pytest
import os


def test_read_anndata(anndata_app_dir, anndata_data_root):
#    pytest.fail(f"appdir:  {anndata_app_dir},  data_root: {anndata_data_root}")
    fg = FGProcess(anndata_app_dir, anndata_data_root)
    assert not fg is None 
    ad_input =  fg.input['some_anndata_input']
    assert ad_input.type == 'anndata'
    anndata = fgad.read_anndata(ad_input)

    assert not anndata is None
    assert anndata.n_obs == 1
    assert anndata.n_vars == 9


def test_write_anndata(anndata_app_dir, anndata_data_root):
    fg = FGProcess(anndata_app_dir, anndata_data_root)
    assert not fg is None 

    ad_output =  fg.output['some_anndata_output']
    assert ad_output.type == 'anndata'
    if os.path.isfile(ad_output.path):
        os.remove(ad_output.path)
    assert not os.path.isfile(ad_output.path)

    ad_input =  fg.input['some_anndata_input']
    assert ad_input.type == 'anndata'
    anndata = fgad.read_anndata(ad_input)

    fgad.write_anndata(anndata, ad_output)
    assert os.path.isfile(ad_output.path)


def test_read_data(anndata_app_dir, anndata_data_root):
    fg = FGProcess(anndata_app_dir, anndata_data_root)
    data = fgad.read_data(fg)
    
    assert not data is None
    assert data.n_obs == 1
    assert data.n_vars == 9


def test_write_data(anndata_app_dir, anndata_data_root):
    fg = FGProcess(anndata_app_dir, anndata_data_root)
    assert not fg is None 

    ad_output =  fg.output['some_anndata_output']
    assert ad_output.type == 'anndata'
    if os.path.isfile(ad_output.path):
        os.remove(ad_output.path)
    assert not os.path.isfile(ad_output.path)

    ad_input =  fg.input['some_anndata_input']
    assert ad_input.type == 'anndata'
    anndata = fgad.read_anndata(ad_input)

    fgad.write_data(fg, anndata)

    assert os.path.isfile(ad_output.path)


def test_read_data_too_many_files(fgprocess_anndata_tmf):
    with pytest.raises(Exception):
        fgad.read_data(fgprocess_anndata_tmf)


def test_write_data_too_many_files(fgprocess_anndata_tmf):
    ad_input =  fgprocess_anndata_tmf.input['some_anndata_input']  
    anndata = fgad.read_anndata(ad_input)

    with pytest.raises(Exception):
        fgad.write_data(fgprocess_anndata_tmf, anndata)


def test_read_data_wrong_type(fgprocess_anndata_wt):
    with pytest.raises(Exception):
        fgad.read_data(fgprocess_anndata_wt)


def test_write_data_wrong_type(fgprocess_anndata_wt):
    with pytest.raises(Exception):
        fgad.write_data(fgprocess_anndata_wt, None)
