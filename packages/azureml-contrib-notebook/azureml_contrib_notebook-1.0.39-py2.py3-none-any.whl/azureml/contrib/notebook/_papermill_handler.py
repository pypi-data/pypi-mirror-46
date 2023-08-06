# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import json
from azureml.contrib.notebook._notebook_handler import NotebookExecutionHandler, _insert_suffix


class PapermillExecutionHandler(NotebookExecutionHandler):
    """Papermill-based notebook execution handler.

    .. remarks::

         .. code-block:: python

             # Import dependencies
             from azureml.core import Workspace, Experiment, RunConfiguration
             from azureml.contrib.notebook import NotebookRunConfig, PapermillExecutionHandler

             # Create new experiment
             workspace = Workspace.from_config()
             exp = Experiment(workspace, "pm_handler_experiment")

             # Customize run configuration to execute in user managed environment
             run_config_user_managed = RunConfiguration()
             run_config_user_managed.environment.python.user_managed_dependencies = True

             # Instante papermill handler with custom kernel
             pm_handler = PapermillExecutionHandler(kernel_name="python3", progress_bar=False)

             # Create notebook run configuration
             cfg = NotebookRunConfig(source_directory="./notebooks",
                                     notebook="notebook-sample.ipynb",
                                     handler=pm_handler,
                                     run_config=run_config_user_managed)

             # Submit experiment and wait for completion
             run = exp.submit(cfg)
             run.wait_for_completion(show_output=True)

    :param history: Enable metrics logs to run history. Enabled by default
    :type history: bool
    :param kwargs: Dictionary of papermill parameters
    :type path: dict
    """

    known_pm_options = ["engine_name",
                        "prepare_only",
                        "kernel_name",
                        "progress_bar",
                        "log_output",
                        "start_timeout",
                        "report_mode",
                        "cwd"]

    def __init__(self, history=True, **kwargs):
        """Construct PapermillExecutionHandler object."""
        super().__init__(os.path.join(os.path.dirname(__file__),
                                      "_handlers",
                                      "papermill_notebook_run_handler.py"))

        for key, val in kwargs.items():
            if key not in self.known_pm_options:
                raise Exception("Unknown Papermill option: {}".format(key))

        self.papermill_args = kwargs
        self.execution_args = {"history": history}
        self.dependencies.append("papermill")
        self.dependencies.append("nteract-scrapbook")
        self.dependencies.append("ipykernel")

    def argument_handling_contract(self, notebook, output_notebook, parameters=None):
        """Return list of arguments in handler accepted format.

        :param notebook: Input notebook
        :type path: str
        :param output_notebook: Output notebook
        :type path: str
        :param parameters: Dictionary of parameters
        :type path: dict

        :return: List of parameters.
        :rtype: list
        """
        if not output_notebook:
            output_notebook = _insert_suffix(notebook)

        return ["-i", notebook,
                "-o", output_notebook,
                "-e", json.dumps(self.execution_args),
                "-p", json.dumps(self.papermill_args),
                "-n", json.dumps(parameters)]
