import fastgenomics.external.anndata as fgad
import pytest
import pandas as pd
import numpy as np


@pytest.mark.anndata
def test_read(fgprocess_1):
    adata = fgad.read(
        expr=fgprocess_1.input["some_input"],
        gene_meta=fgprocess_1.input["genes"],
        cell_meta=fgprocess_1.input["cells"],
    )

    assert adata.obs.index.equals(pd.Index(["c1", "c3", "c4", "c2"]))
    assert adata.var.index.equals(
        pd.Index(["1", "3", "5", "10", "100", "unknown", "unknown", "ambiguous"])
    )
    assert adata.X[1, 0] == 4
    assert adata.shape == (4, 8)
    assert adata.var.shape[1] == 3
    assert adata.obs.shape[1] == 3
    assert "some_column" in adata.var
    assert "some_column" in adata.obs
    assert "batch_id" in adata.obs


@pytest.mark.anndata
def test_read_colnames(fgprocess_1_colnames):
    adata = fgad.read(
        expr=fgprocess_1_colnames.input["some_input"],
        gene_meta=fgprocess_1_colnames.input["genes"],
        cell_meta=fgprocess_1_colnames.input["cells"],
        gene_id="gene_id_1",
        cell_id="cell_id_1",
        expression_id="expression_id_1",
    )

    assert adata.obs.index.equals(pd.Index(["c1", "c3", "c4", "c2"]))
    assert adata.var.index.equals(
        pd.Index(["1", "3", "5", "10", "100", "unknown", "unknown", "ambiguous"])
    )
    assert adata.X[1, 0] == 4
    assert adata.shape == (4, 8)
    assert adata.var.shape[1] == 3
    assert adata.obs.shape[1] == 3
    assert "some_column" in adata.var
    assert "some_column" in adata.obs
    assert "batch_id" in adata.obs


@pytest.mark.anndata
def test_read_partial(fgprocess):
    fgad.read(expr=fgprocess.input["some_input"])
    fgad.read(expr=fgprocess.input["some_input"], gene_meta=fgprocess.input["genes"])
    fgad.read(expr=fgprocess.input["some_input"], cell_meta=fgprocess.input["cells"])
    fgad.read(
        expr=fgprocess.input["some_input"],
        cell_meta=fgprocess.input["non_existing_optional_input"],
        gene_meta=fgprocess.input["non_existing_optional_input"],
    )


@pytest.mark.anndata
def test_read_type_throws(fgprocess):
    with pytest.raises(TypeError):
        fgprocess.input["some_input"].type = "wrong_type"
        fgad.read(
            expr=fgprocess.input["some_input"],
            gene_meta=fgprocess.input["genes"],
            cell_meta=fgprocess.input["cells"],
        )


@pytest.mark.anndata
def test_write(fgprocess, adata):
    for f in ["count_output", "genes_output", "cells_output"]:
        assert not fgprocess.output[f].path.exists()

    fgad.write(
        adata,
        expr=fgprocess.output["count_output"],
        gene_meta=fgprocess.output["genes_output"],
        cell_meta=fgprocess.output["cells_output"],
    )

    for f in ["count_output", "genes_output", "cells_output"]:
        assert fgprocess.output[f].path.exists()


@pytest.mark.anndata
def test_read_write(fgprocess_1, adata_1):
    fgad.write(
        adata_1,
        expr=fgprocess_1.output["count_output"],
        gene_meta=fgprocess_1.output["genes_output"],
        cell_meta=fgprocess_1.output["cells_output"],
    )

    expr_out = pd.read_csv(
        fgprocess_1.output["count_output"].path,
        dtype={
            "entrez_id": "category",
            "cell_id": "category",
            "expression": np.float64,
        },
    )
    expr_out = expr_out.sort_values(list(expr_out.columns)).reset_index(drop=True)

    genes_out = pd.read_csv(
        fgprocess_1.output["genes_output"].path, dtype={"entrez_id": "category"}
    )
    genes_out.set_index("entrez_id", inplace=True, drop=False)

    cells_out = pd.read_csv(
        fgprocess_1.output["cells_output"].path, dtype={"cell_id": "category"}
    )
    cells_out.set_index("cell_id", inplace=True, drop=False)

    expr_in = pd.DataFrame(
        dict(
            cell_id=pd.Categorical(["c1", "c1", "c2", "c3", "c3"]),
            entrez_id=pd.Categorical(["1", "3", "5", "1", "100"]),
            expression=[1.0, 2.0, 3.0, 4.0, 1.0],
        )
    )
    expr_in = expr_in.sort_values(list(expr_out.columns)).reset_index(drop=True)

    assert expr_out.equals(expr_in)
    assert genes_out.equals(adata_1.var)
    assert cells_out.equals(adata_1.obs)


@pytest.mark.anndata
def test_preserve_column_order(fgprocess):
    adata = fgad.read(
        expr=fgprocess.input["some_input"],
        gene_meta=fgprocess.input["genes"],
        cell_meta=fgprocess.input["cells"],
    )

    fgad.write(
        adata,
        expr=fgprocess.output["count_output"],
        gene_meta=fgprocess.output["genes_output"],
        cell_meta=fgprocess.output["cells_output"],
    )

    assert (
        fgprocess.input["genes"].path.read_text()
        == fgprocess.output["genes_output"].path.read_text()
    )

    assert (
        fgprocess.input["cells"].path.read_text()
        == fgprocess.output["cells_output"].path.read_text()
    )
