from mlspeclib import MLSchema, MLObject
from random import randint, random, randrange
from pathlib import Path
import datetime
import uuid

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
subprocess = MagicMock()
popen_return = MagicMock()
popen_return.stdout.read.return_value = "Popen job result would go here."
popen_return.stdout.job_id.return_value = uuid.uuid4().hex  # Fake hash

subprocess.Popen.return_value = popen_return
timer = MagicMock()

# Below is for testing - comment out when live
# input_object = MagicMock()
# execution_object = MagicMock()
# results_ml_object = MagicMock()
# result_ml_object_schema_type = 'feature_engineering_result'
# result_ml_object_schema_version = '2.1.0'

results_ml_object.set_type(
    schema_type=result_ml_object_schema_type,  # noqa
    schema_version=result_ml_object_schema_version,  # noqa
)

# Mocked up execution
pipeline_name = "filter_and_tokenize"
repo_hash = "b52063c"

# Below is how you would execute a Pachyderm data processing job on a Pachyderm deployment
external_command = f"pachctl run pipeline {pipeline_name} repo@{repo_hash} inputs={input_object.to_json()}"
result_of_start_pipeline_command = subprocess.Popen(
    external_command, shell=True, stdout=subprocess.PIPE
).stdout.read()

results_ml_object.extended_properties = {}
results_ml_object.extended_properties['result_of_start_pipeline_command'] = result_of_start_pipeline_command
job_id = subprocess.Popen(
    external_command, shell=True, stdout=subprocess.PIPE
).stdout.job_id()

return_dict = {}
finished_time = None
while finished_time is None:
    external_command = f"pachctl query job id={job_id}"
    results_ml_object.extended_properties['job_finished'] = subprocess.Popen(
        external_command, shell=True, stdout=subprocess.PIPE
    ).stdout.read()
    if results_ml_object.extended_properties['job_finished'] is not None:
        finished_time = datetime.datetime.now()

# We're mocking up the idea that the data is all being written to a common share.
# This could come from Pachyderm directly (we'd do something like the following)
#
#     external_command = f"pachctl get job-information id={job-info}"
#     return_dict = subprocess.Popen(
#         external_command, shell=True, stdout=subprocess.PIPE
#     ).stdout.read()

return_dict = {
    "data_output_path": str(Path("/data/contoso/bork_model/raw_data/").absolute()),
    "data_statistics_path": str(
        Path("/data/contoso/bork_model/statistics/").absolute()
    ),
    "data_schemas_path": str(Path("/data/contoso/bork_model/schemas/").absolute()),
    "feature_file_path": str(Path("/data/contoso/bork_model/features/").absolute()),
    "engineered_data_path": str(
        Path("/data/contoso/bork_model/engineered_data/").absolute()
    ),
    "feature_engineering_steps": [
        'r"[^\x00-\x7F]+"   # Filter sentences with non-Ascii',
        "tokenize_for_bigrams(sentence)  # returns a tokenized sentence",
        "eliminate_stop_words(sentence)  # detects stop words and eliminates them if necessary",
    ],
}

results_ml_object.data_output_path = return_dict["data_output_path"]
results_ml_object.data_statistics_path = return_dict["data_statistics_path"]
results_ml_object.data_schemas_path = return_dict["data_schemas_path"]
results_ml_object.feature_file_path = return_dict["feature_file_path"]

# NEW FIELDS
results_ml_object.engineered_data_path = return_dict["engineered_data_path"]
results_ml_object.feature_engineering_steps = return_dict["feature_engineering_steps"]
results_ml_object.extended_properties['finished_time'] = finished_time

# Execution metrics
results_ml_object.execution_profile.system_memory_utilization = random()
results_ml_object.execution_profile.network_traffic_in_bytes = randint(7e9, 9e10)
results_ml_object.execution_profile.gpu_temperature = randint(70, 130)
results_ml_object.execution_profile.disk_io_utilization = random()
results_ml_object.execution_profile.gpu_percent_of_time_accessing_memory = random()
results_ml_object.execution_profile.cpu_utilization = random()
results_ml_object.execution_profile.gpu_utilization = random()
results_ml_object.execution_profile.gpu_memory_allocation = random()
