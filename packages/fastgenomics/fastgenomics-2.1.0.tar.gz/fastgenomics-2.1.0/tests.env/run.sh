#!/bin/bash

export FG_TEST_DIR=tests/
export FG_DATA_ROOT=$FG_TEST_DIR/data/working_1_no_mapping
export FG_APP_DIR=$FG_TEST_DIR/apps/working
export SOME_VAR=../data
export INPUT_FILE_MAPPING='
{
    "some_input": "$SOME_VAR/expression_matrix.csv",
    "cells": "cell_metadata.csv",
    "genes": "$SOME_VAR/gene_metadata.csv",
    "some_optional_input": "optional_existing"
}
'

python3 -m pytest tests.env
