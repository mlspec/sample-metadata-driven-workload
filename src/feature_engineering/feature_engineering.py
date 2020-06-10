from mlspeclib import MLSchema, MLObject
from random import randint, random, randrange
from pathlib import Path
import datetime
import uuid

# THIS IS A MOCKED UP FILE. IT DOES NOT REPRESENT THE NOTEBOOK BEING EXECUTED AND IS FOR THE PURPOSE OF DEMO ONLY.

results_ml_object.set_type(
    schema_type=result_ml_object_schema_type,  # noqa
    schema_version=result_ml_object_schema_version,  # noqa
)

# Mocked up results
return_dict = {
    "data_output_path": str(Path("/data/contoso/bork_model/raw_data/").absolute()),
    "data_statistics_path": str(
        Path("/data/contoso/bork_model/statistics/").absolute()
    ),
    "data_schemas_path": str(Path("/data/contoso/bork_model/schemas/").absolute()),
    "feature_file_path": str(Path("/data/contoso/bork_model/features/").absolute()),
    "engineered_data_path": str(Path("/data/contoso/bork_model/engineered_data/").absolute()),
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
results_ml_object.extended_properties = {}

# Execution metrics
results_ml_object.execution_profile.system_memory_utilization = random()
results_ml_object.execution_profile.network_traffic_in_bytes = randint(7e9, 9e10)
results_ml_object.execution_profile.gpu_temperature = randint(70, 130)
results_ml_object.execution_profile.disk_io_utilization = random()
results_ml_object.execution_profile.gpu_percent_of_time_accessing_memory = random()
results_ml_object.execution_profile.cpu_utilization = random()
results_ml_object.execution_profile.gpu_utilization = random()
results_ml_object.execution_profile.gpu_memory_allocation = random()
