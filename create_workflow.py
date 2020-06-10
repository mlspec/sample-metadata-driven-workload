import sys
from pathlib import Path
import yaml as YAML
import uuid
import datetime
from mlspeclib import MLObject, MLSchema, Metastore
from tests.metastore_credentials import Credentials

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / "bin"))

# from utils import setupLogger  # noqa


def main():
    MLSchema.append_schema_to_registry(Path(".parameters") / "schemas")

    workflow_version = "2.0.0"
    workflow_path = (Path(".parameters") / "workflow_2_2_0.yaml")
    workflow_input_string = YAML.safe_dump(workflow_path.read_text())
    workflow_dict = YAML.safe_load(YAML.safe_load(workflow_input_string))
    workflow_dict["workflow_version"] = workflow_version
    workflow_dict["run_id"] = str(uuid.uuid4())
    workflow_dict["step_id"] = str(uuid.uuid4())
    workflow_dict["run_date"] = datetime.datetime.now()

    workflow_string = YAML.safe_dump(workflow_dict)
    (workflow_object, errors) = MLObject.create_object_from_string(workflow_string)

    credentials_packed = Credentials.metastore_credentials_prod
    ms = Metastore(credentials_packed)

    workflow_node_id = ms.create_workflow_node(workflow_object, workflow_dict["run_id"])
    ms.create_workflow_steps(workflow_node_id, workflow_object)
    print(f"Success {str(workflow_path)} - workflow_node_id: {workflow_node_id}")


if __name__ == "__main__":
    main()
