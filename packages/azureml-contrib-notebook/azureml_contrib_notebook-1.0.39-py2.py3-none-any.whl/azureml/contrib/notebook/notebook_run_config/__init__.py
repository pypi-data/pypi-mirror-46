# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""DEPRECATED. Use azureml.contrib.notebook for imports."""
from azureml.contrib.notebook._notebook_handler import NotebookExecutionHandler
from azureml.contrib.notebook._notebook_run_config import NotebookRunConfig
from azureml.contrib.notebook._papermill_handler import PapermillExecutionHandler

import warnings
msg = "azureml.contrib.notebook.notebook_run_config module is deprecated. "\
    "Use azureml.contrib.notebook for all imports"
warnings.warn(msg)


__all__ = [
    "NotebookExecutionHandler",
    "NotebookRunConfig",
    "PapermillExecutionHandler"
]
