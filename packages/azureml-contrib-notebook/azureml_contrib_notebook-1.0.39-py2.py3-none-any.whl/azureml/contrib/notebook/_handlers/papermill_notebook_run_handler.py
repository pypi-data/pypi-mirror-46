# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Execute notebook with papermill."""
import argparse
import json


def execute_notebook(source_notebook, destination_notebook, infra_args, papermill_args, notebooks_args):
    """Execute notebook with papermill.

    :param source_notebook: Source notebook file name
    :type source_notebook: str
    :param destination_notebook: Source notebook file name
    :type destination_notebook: str
    :param infra_args: Infrastructure arguments
    :type infra_args: dict
    :param papermill_args: Papermill arguments
    :type papermill_args: dict
    :param notebooks_args: Notebook arguments
    :type notebooks_args: dict
    """
    import papermill as pm
    import scrapbook as sb

    # if kernel name is specified
    kernel_name = papermill_args.get("kernel_name")

    # if not specified try to get it from the notebook
    if not kernel_name:
        with open(source_notebook) as nbfile:
            notebook = json.loads(nbfile.read())
        try:
            kernel_name = notebook.get("metadata").get("kernelspec").get("name")
        except:
            pass

    # create a kernel spec if not installed
    try:
        if kernel_name:
            from jupyter_client.kernelspec import KernelSpecManager
            if not KernelSpecManager().get_all_specs().get(kernel_name):
                # TODO: replace jupyter_client.kernelspec.KernelSpecManager logic
                from ipykernel.kernelspec import install
                install(kernel_name=kernel_name)
            papermill_args["kernel_name"] = kernel_name
    except:
        pass

    # execute notebook
    pm.execute_notebook(
        source_notebook,
        destination_notebook,
        parameters=notebooks_args,
        **papermill_args
    )

    # TODO scrapbook
    if infra_args.get("history"):
        batchsize = 50
        from azureml.core import Run
        results = sb.read_notebook(destination_notebook)
        run = Run.get_context()
        for key, value in results.scraps.items():
            scrap = value
            if isinstance(scrap.data, list):
                for index in range(0, len(scrap.data), batchsize):
                    run.log_list(scrap.name, scrap.data[index:index + batchsize])
            else:
                run.log(scrap.name, scrap.data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", default="",
                        help="input notebook")
    parser.add_argument("-o", "--output", default="",
                        help="output notebook")
    parser.add_argument("-e", "--execution_args", default="",
                        help="execution options")
    parser.add_argument("-p", "--papermill_args", default="",
                        help="papermill arguments")
    parser.add_argument("-n", "--notebook_args", default="",
                        help="notebook parameters")

    args = parser.parse_args()

    execute_notebook(args.input, args.output,
                     json.loads(args.execution_args),
                     json.loads(args.papermill_args),
                     json.loads(args.notebook_args))
