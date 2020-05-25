from pathlib import Path
import sys
import yaml as YAML
import datetime
import random
import uuid
import hashlib
from mlspeclib import MLObject, MLSchema
from metastore_credentials import Credentials
import subprocess
import re
import base64

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / "bin"))

from utils import setupLogger, random_item_from_list  # noqa


class Workflow:
    rootLogger = None
    buffer = None

    def __init__(self):
        (self.rootLogger, self.buffer) = setupLogger()

    def main(self):

"""
- Dashboard for runs
-- Size
-- Likelihood of bias
-- Time for run
-- Accuracy
- Filter by version
- Look up at top version and show metadata going in and out

- Show bad input (e.g. it's null) and what happens when you run it
- Show when you add a new step - how you can compare those with other versions

"""
        MLSchema.append_schema_to_registry(Path(".parameters") / "schemas")

        repo_name = "mlspec"
        output_regex = "::set-output name=output_base64_encoded::(.*?)\\\\"

        run_date_start = datetime.datetime(2020, 1, 1) + datetime.timedelta(
            seconds=random.randrange(0, 5184000)
        )
        run_id = str(uuid.uuid4())

        step_name = "process_data"
        data_source = MLObject()
        data_source.set_type("500.0.1", "data_source")
        data_source.run_id = run_id
        data_source.step_id = str(uuid.uuid4())
        data_source.run_date = str(run_date_start.isoformat())
        data_source.source_id = str(uuid.uuid4())
        data_source.source_uri = f"https://internal.contoso.com/datasets/raw_nlp_data-{run_date_start.strftime('%Y-%m-%d')}-{get_random_md5()}"  # noqa
        data_source.extended_properties = {}

        data_process_run = MLObject()
        data_process_run.set_type("500.0.1", "data_process_run")
        data_process_run.nodes = random.randrange(1, 4) * 2
        data_process_run.cpu_per_node = f"{random.randrange(2,8) * 2}"
        data_process_run.ram_per_node = f"{random.randrange(1,16) * 8}Gi"
        data_process_run.gpu_required = (random.randrange(1, 2) % 2) == 0
        data_process_run.output_root_path = (
            "https://internal.contoso.com/datasets/processed_data/"
        )
        data_process_run.base_image = random_base_image()
        data_process_run.machine_type = random_machine_type()
        data_process_run.run_id = run_id
        data_process_run.step_id = str(uuid.uuid4())
        data_process_run.run_date = str(run_date_start.isoformat())
        data_process_run.extended_properties = {}

        environment_dict = YAML.safe_load(
            f"""
INPUT_schemas_directory: '.parameters/schemas'
# INPUT_schemas_git_url: 'https://github.com:mlspec/mlspeclib-action-samples-schemas.git'
INPUT_schemas_git_url: 'https://github.com/mlspec/mlspeclib-action-samples-schemas.git'
INPUT_workflow_node_id: 'workflow|500.0.1|5d265f44-b919-4882-96c2-32799a7b7b76'
INPUT_step_name: {step_name}
INPUT_input_parameters_raw: {data_source.dict_without_internal_variables()}
INPUT_execution_parameters_raw: {data_process_run.dict_without_internal_variables()}
INPUT_METASTORE_CREDENTIALS: {Credentials.metastore_credentials}
GITHUB_RUN_ID: {str(run_id)}
GITHUB_WORKSPACE: '/src'
        """
        )

        self.run_container(
            repo_name, "mlspeclib-action-samples-process-data", environment_dict
        )

        buff_val = self.buffer.getvalue()
        m = re.search(output_regex, buff_val)
        process_data_encoded_val = m.group(1)

        # Below is for debugging, we're ok leaving it in base64 encoded
        process_data_output_value = base64.urlsafe_b64decode(process_data_encoded_val)
        self.buffer.truncate(0)
        self.buffer.seek(0)

        step_name = "train"
        training_run = MLObject()
        training_run.set_type("500.0.1", "training_run")
        training_run.nodes = 8
        training_run.cpu_per_node = 8
        training_run.ram_per_node = "64Gi"
        training_run.gpu_required = True
        training_run.output_path = "test/models/output"
        training_run.training_params.learning_rate = 0.1
        training_run.training_params.loss = 0.3
        training_run.training_params.batch_size = 1000
        training_run.training_params.epoch = 50
        training_run.training_params.optimizer = ["SGD"]
        training_run.training_params.other_tags = {"pii": False, "data_sha": "8b03f70"}
        training_run.extended_properties = {}

        environment_dict_train = YAML.safe_load(
            f"""
INPUT_schemas_directory: '.parameters/schemas'
INPUT_schemas_git_url: 'https://github.com/mlspec/mlspeclib-action-samples-schemas.git'
INPUT_workflow_node_id: 'workflow|500.0.1|5d265f44-b919-4882-96c2-32799a7b7b76'
INPUT_step_name: {step_name}
INPUT_input_parameters_base64: {process_data_encoded_val}
INPUT_execution_parameters_raw: {training_run.dict_without_internal_variables()}
INPUT_METASTORE_CREDENTIALS: {Credentials.metastore_credentials}
GITHUB_RUN_ID: {str(run_id)}
GITHUB_WORKSPACE: '/src'
        """
        )

        self.run_container(
            repo_name, "mlspeclib-action-samples-train", environment_dict_train
        )

        buff_val = self.buffer.getvalue()
        m = re.search(output_regex, buff_val)
        train_encoded_val = m.group(1)
        train_output_value = base64.urlsafe_b64decode(train_encoded_val)
        self.buffer.truncate(0)
        self.buffer.seek(0)

        step_name = "package"
        package_run = MLObject()
        package_run.set_type("500.0.1", "package_run")
        package_run.run_id = run_id
        package_run.step_id = str(uuid.uuid4())
        package_run.run_date = run_date_start.isoformat()
        package_run.model_source = '/nfs/trained_models/nlp'
        package_run.container_registry = f"https://registry.hub.docker.com/v1/repositories/contoso/nlp/{get_random_md5()}"  # noqa
        package_run.agent_pool = f"nlp-build-pool"
        package_run.build_args = ["arg1", "arg2", "arg3"]
        package_run.extended_properties = {}
        package_run.secrets = {'credentials': 'AZURE_CREDENTIALS', 'docker_username': 'DOCKERUSERNAME', 'docker_password': 'DOCKERPASSWORD'}

        environment_dict_package = YAML.safe_load(
            f"""
INPUT_schemas_directory: '.parameters/schemas'
INPUT_schemas_git_url: 'https://github.com/mlspec/mlspeclib-action-samples-schemas.git'
INPUT_workflow_node_id: 'workflow|500.0.1|5d265f44-b919-4882-96c2-32799a7b7b76'
INPUT_step_name: {step_name}
INPUT_input_parameters_base64: {train_encoded_val}
INPUT_execution_parameters_raw: {package_run.dict_without_internal_variables()}
INPUT_METASTORE_CREDENTIALS: {Credentials.metastore_credentials}
GITHUB_RUN_ID: {str(run_id)}
GITHUB_WORKSPACE: '/src'
        """
        )

        self.run_container(
            repo_name, "mlspeclib-action-samples-package", environment_dict_package
        )

        buff_val = self.buffer.getvalue()
        m = re.search(output_regex, buff_val)
        encoded_val = m.group(1)
        print(base64.urlsafe_b64decode(encoded_val))
        self.buffer.flush()

    def run_container(
        self, repo_name: str, container_name: str, environement_dict: dict
    ):
        environment_vars_list = []
        debug_env_string = ""
        for entry in environement_dict:
            if isinstance(environement_dict[entry], dict):
                env_value = YAML.safe_dump(environement_dict[entry])
            else:
                env_value = environement_dict[entry]
            environment_vars_list.append("-e")
            environment_vars_list.append(f"{entry}={env_value}")
            debug_env_string += f' -e "{entry}={env_value}"'

        exec_statement = (
            ["docker", "run"]
            + environment_vars_list
            + [f"{repo_name}/{container_name}"]
        )

        print(
            f"docker run \\\n {debug_env_string} \\\n -ti --entrypoint=/bin/bash {repo_name}/{container_name}"
        )

        p = subprocess.Popen(
            exec_statement, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = p.communicate()
        self.rootLogger.debug(f"out = {str(out)}")
        self.rootLogger.debug(f"error = {str(err)}")
        # self.assertTrue(str(err, "utf-8") == "")


def random_base_image():
    base_image_list = [
        "bionic-20200403",
        "eoan-20200410",
        "focal-20200423",
        "groovy-20200505",
        "trusty-20191217",
        "xenial-20200326",
    ]
    return random_item_from_list(base_image_list)


def random_machine_type():
    machine_type_list = ["ND6s", "ND12s", "ND24rs", "ND24s"]
    return random_item_from_list(machine_type_list)


def get_random_md5():
    return hashlib.md5(str(random.randrange(0, 2e20)).encode('utf-8')).hexdigest()

if __name__ == "__main__":
    workflow_executor = Workflow()
    workflow_executor.main()
