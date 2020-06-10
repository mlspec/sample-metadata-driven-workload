from mlspeclib import MLSchema, MLObject
from random import randint, random, randrange
from pathlib import Path
import uuid
import datetime

from unittest.mock import MagicMock

# This file has the following variables:
#         workflow_object = an MLObject of the current workflow
#         input_object = an MLObject of the current input to this step
#         execution_object = an MLObject of the current execution to this step
#         step_name = string of the name of this step.
#         parameters.GITHUB_RUN_ID = a UUID of this run (provided by Github)
#
# Additionally, GitHub provides a number of variables as environement variables including:
#
#     CI	                Always set to true.
#     HOME	                The path to the GitHub home directory used to store user data. For example, /github/home.
#     GITHUB_WORKFLOW	    The name of the workflow.
#     GITHUB_RUN_ID	        A unique number for each run within a repository. This number does not change if you re-run the workflow run.
#     GITHUB_RUN_NUMBER	    A unique number for each run of a particular workflow in a repository. This number begins at 1 for the workflow's first run,
#                           and increments with each new run. This number does not change if you re-run the workflow run.
#     GITHUB_ACTION	        The unique identifier (id) of the action.
#     GITHUB_ACTIONS	    Always set to true when GitHub Actions is running the workflow. You can use this variable to differentiate when tests are
#                           being run locally or by GitHub Actions.
#     GITHUB_ACTOR	        The name of the person or app that initiated the workflow. For example, octocat.
#     GITHUB_REPOSITORY	    The owner and repository name. For example, octocat/Hello-World.
#     GITHUB_EVENT_NAME	    The name of the webhook event that triggered the workflow.
#     GITHUB_EVENT_PATH	    The path of the file with the complete webhook event payload. For example, /github/workflow/event.json.
#     GITHUB_WORKSPACE	    The GitHub workspace directory path. The workspace directory contains a subdirectory with a copy of your repository if your
#                           workflow uses the actions/checkout action. If you don't use the actions/checkout action, the directory will be empty.
#                           For example, /home/runner/work/my-repo-name/my-repo-name.
#     GITHUB_SHA	        The commit SHA that triggered the workflow. For example, ffac537e6cbbf934b08745a378932722df287a53.
#     GITHUB_REF	        The branch or tag ref that triggered the workflow. For example, refs/heads/feature-branch-1. If neither a branch or tag is
#                           available for the event type, the variable will not exist.
#     GITHUB_HEAD_REF	    Only set for forked repositories. The branch of the head repository.
#     GITHUB_BASE_REF	    Only set for forked repositories. The branch of the base repository.
#
# You can read more about these here - https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables

# The code below is for mocking to make the rest of the code look legit
# subprocess = MagicMock()
# popen_return = MagicMock()
# popen_return.stdout.read.return_value = "Popen job result would go here."
# subprocess.Popen.return_value = popen_return
# timer = MagicMock()


# Below is for testing - comment out when live
# input_object = MagicMock()
# execution_object = MagicMock()
# results_ml_object = MagicMock()
# result_ml_object_schema_type = 'feature_engineering_result'
# result_ml_object_schema_version = '2.1.0'

results_ml_object.set_type(
    schema_type=result_ml_object_schema_type,
    schema_version=result_ml_object_schema_version,
)

# Below mocks out the result of packaging - these might be the outputs of a build step
return_dict = YAML.safe_load(
    """
servable: True
package_size: 1029310298
tested_platforms: ['kubeflow', 'azureml', 'sagemaker']
model_source:
    servable_model:
        data_store: 's3'
        bucket: 'nlg-bucket'
        path: 'a231653454ca8e07f42adc7941aeec6b'
serving_container_image:
    container_image_url: 'https://hub.docker.com/repository/docker/contoso/nlg-bork'
"""
)
finished_time = datetime.datetime.now().isoformat()

results_ml_object.servable = return_dict["servable"]
results_ml_object.tested_platforms = return_dict["tested_platforms"]
results_ml_object.package_size = return_dict["package_size"]
results_ml_object.model_source.servable_model.data_store = return_dict["model_source"][
    "servable_model"
]["data_store"]
results_ml_object.model_source.servable_model.bucket = return_dict["model_source"][
    "servable_model"
]["bucket"]
results_ml_object.model_source.servable_model.path = return_dict["model_source"][
    "servable_model"
]["path"]
results_ml_object.serving_container_image.container_image_url = return_dict[
    "serving_container_image"
]["container_image_url"]
results_ml_object.extended_properties = {'finished_time': finished_time}

# Execution metrics
results_ml_object.execution_profile.system_memory_utilization = random()
results_ml_object.execution_profile.network_traffic_in_bytes = randint(7e9, 9e10)
results_ml_object.execution_profile.gpu_temperature = randint(70, 130)
results_ml_object.execution_profile.disk_io_utilization = random()
results_ml_object.execution_profile.gpu_percent_of_time_accessing_memory = random()
results_ml_object.execution_profile.cpu_utilization = random()
results_ml_object.execution_profile.gpu_utilization = random()
results_ml_object.execution_profile.gpu_memory_allocation = random()
