[![pypi-shield]][pypi]
[![travis-shield]][travis]
[![docs-shield]][docs]

[pypi-shield]: https://img.shields.io/pypi/v/fastgenomics.svg
[pypi]: https://pypi.org/project/fastgenomics
[travis-shield]: https://travis-ci.org/FASTGenomics/fastgenomics-py.svg?branch=master
[travis]: https://travis-ci.org/FASTGenomics/fastgenomics-py
[docs-shield]: https://readthedocs.org/projects/fastgenomics/badge/?version=latest
[docs]: http://fastgenomics.readthedocs.io

# About

This python module handles all common interfaces
of your application to the FASTGenomics runtime:

-  Input/Output of files
-  Parameters

and provides some convenience functions.

## Examples

A basic interaction through the `fastgenomics` module looks looks this

``` python
from fastgenomics.process import FGProcess

app_dir = "app_directory/"
data_dir = "data_directory/"
fg = FGProcess(app_dir, data_dir)

# access a parameter
fg.parameters["some_parameter"]

# access an input/ouput file
fg.input["some_input_file.txt"].path
fg.output["some_output_file.txt"].path
```

### Consistency checks

The constructor of `FGProcess` will check if all the necessary files
exist and validate if their content is according to the FASTGenomics
standard.  For example, if you make a mistake in the `manifest.json`
you will get a relevant error when calling `FGProcess`.

### Reading & Writing AnnData
You can also easily load an AnnData object with

``` python
from fastgenomics.external import anndata

# read AnnData
adata = anndata.read(
            expr=fg.input["expression_matrix"],
            gene_meta=fg.input["genes"],
            cell_meta=fg.input["cells"],
        )

# write AnnData
anndata.write(
        adata,
        expr=fg.output["expression_matrix"],
        gene_meta=fg.output["genes_output"],
        cell_meta=fg.output["cells_output"],
    )
```

In the `read` the `cell_metadata` and `gene_metadata` are optional, in
the `write` all the outputs are optional.

_note_ This functionality is kept in a separate submodule, to keep the
dependency on scanpy optional.

### Parameter checks

Aside from accessing the parameters you can also use the following
function to validate if a parameter fulfills some arbitrary
constraints.  The code below raises a `ValueError` when
`some_parameter` is not larger then zero.

``` python
fg.parametres.check(
    "some_parameter",
    lambda x: x > 0,
    'Parameter "some_parameter" must be larger then 0.')
```

### Writing the summary with a jinja2 template
FASTGenomics requires an app to output a `summary.md` file, this file
is typically generated using a [jinja2
template](http://jinja.pocoo.org/).  This module provides the
following utility function for generating a summary file.

``` python
fg.summary.template = "path_to_the_tempalte/summary.md.j2"
fg.summary.write(some_value=1, some_other_value=2)
```

This generates a `summary.md` file in
`"[data_dir]/summary/summary.md"` based on the template in
`fg.summary.template` passing `some_value=1` and `some_other_value=2`
to the template engine.

*Note:* The `fg.summary.write` function appends a `###`-level section
with the parameter values, with which the app was run.

## Internals

The module encapsulates most of its functionality in a single class
`FGProcess(app_dir, data_dir)` that is constructed from two paths:
`app_dir`, where all the necessary app-related files are (most
importantly, the `manifest.json`) and `data_dir`, which points to the
directory structure provided by FASTGenomics.  The class `FGProcess`
has the following attributes

- `app`: contains the interpreted `manifest.json` and the locations of
  app-related files.
- `parameters`: facilitates the access to parameters provided by the
  FASTGenomics runtime.
- `input`, `output`: represents the input and output files provide by
  the FASTGenomics runtime.
- `summary`: handles the `summary.md` rendering.
