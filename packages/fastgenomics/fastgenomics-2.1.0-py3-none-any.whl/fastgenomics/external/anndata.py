try:
    import pandas as pd
    import numpy as np
    import scipy.sparse as sp
    from anndata import AnnData
except ImportError as e:
    msg = f"Could not import some of the necessary modules ({e.name}).  Please make sure to install anndata (https://github.com/theislab/anndata) with all its dependencies correctly (e.g. pandas, numpy, scipy)."
    raise ImportError(msg, name=e.name, path=e.path)
    raise e


EXPRESSION_MATRIX_DTYPE = {
    "entrez_id": "category",
    "cell_id": "category",
    "expression": np.float64,
}


def check_file_type(file, content_type):
    """Returns a path if the file is of requested FASTGenomics type,
otherwise throws a TypeError."""
    if file.type != content_type:
        raise TypeError(
            f'File "{file.name}" is of type "{file.type}" but expected "{content_type}".'
        )


def read(
    expr,
    cell_meta=None,
    gene_meta=None,
    cell_id="cell_id",
    gene_id="entrez_id",
    expression_id="expression",
):
    """Reads an anndata object by composing three files together:
`expression_matrix`, `cell_metadata` and `gene_metadata`."""
    check_file_type(expr, content_type="expression_matrix")
    expr = pd.read_csv(
        expr.path,
        dtype={cell_id: "category", gene_id: "category", expression_id: np.float32},
    )

    obs = read_cell_metadata(cell_meta, expr, cell_id)
    var = read_gene_metadata(gene_meta, expr, gene_id)

    counts = read_sparse_matrix(expr, obs, var, cell_id, gene_id, expression_id)

    adata = AnnData(counts, obs=obs, var=var, dtype="float32")
    return adata


def read_cell_metadata(cell_meta, expr, cell_id):
    expr_cell_id = expr[cell_id].unique()

    if cell_meta is None or not cell_meta.exists():
        df = pd.DataFrame(data={cell_id: expr_cell_id})
    else:
        check_file_type(cell_meta, content_type="cell_metadata")
        df = pd.read_csv(cell_meta.path, dtype={cell_id: str})

    df[cell_id] = df[cell_id].astype("category")
    df.set_index(cell_id, inplace=True, drop=False)

    missing_ids = set(expr_cell_id) - set(df.index)
    if missing_ids:
        raise Exception(
            f'Some {cell_id}\'s were present in the expression matrix but not in "{cell_meta.path}": {missing_ids}.'
        )
    return df


def read_gene_metadata(gene_meta, expr, gene_id):
    expr_entrez_id = expr[gene_id].unique()

    if gene_meta is None or not gene_meta.exists():
        df = pd.DataFrame(data={gene_id: expr_entrez_id})
    else:
        check_file_type(gene_meta, content_type="gene_metadata")
        df = pd.read_csv(gene_meta.path, dtype={gene_id: str})

    df[gene_id] = df[gene_id].astype("category")
    df.set_index(gene_id, inplace=True, drop=False)

    missing_ids = set(expr_entrez_id) - set(df.index)
    if missing_ids:
        raise Exception(
            f'Some {gene_id}\'s were present in the expression matrix but not in "{gene_meta.path}": {missing_ids}.'
        )

    return df


def read_sparse_matrix(expr, obs, var, cell_id, gene_id, expression_id):
    cell_idx = pd.DataFrame(
        {cell_id: obs.index, "cell_idx": np.arange(obs.shape[0])}
    ).set_index(cell_id)
    gene_idx = pd.DataFrame(
        {gene_id: var.index, "gene_idx": np.arange(var.shape[0])}
    ).set_index(gene_id)
    expr = expr.merge(cell_idx, on=cell_id, copy=False)
    expr = expr.merge(gene_idx, on=gene_id, copy=False)

    counts = sp.coo_matrix(
        (expr[expression_id], (expr.cell_idx, expr.gene_idx)),
        shape=(obs.shape[0], var.shape[0]),
    ).tocsr()

    return counts


# Writing
def write_exprs_csv(adata, csv_file):
    mat = adata.X.tocoo()
    df = pd.DataFrame.from_dict(
        dict(
            cell_id=adata.obs_names[mat.row],
            entrez_id=adata.var_names[mat.col],
            expression=mat.data,
        )
    )
    df.to_csv(csv_file, index=False)


def write(adata, expr=None, cell_meta=None, gene_meta=None):
    if expr is not None:
        check_file_type(expr, content_type="expression_matrix")
        write_exprs_csv(adata, expr.path)

    if cell_meta is not None:
        check_file_type(cell_meta, content_type="cell_metadata")
        adata.obs.to_csv(cell_meta.path, index=False)

    if gene_meta is not None:
        check_file_type(gene_meta, content_type="gene_metadata")
        adata.var.to_csv(gene_meta.path, index=False)
