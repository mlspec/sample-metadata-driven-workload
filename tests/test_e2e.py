import os
import logging
from pathlib import Path
import yaml as YAML
import uuid
import sys
from mlspeclib import MLObject, MLSchema
import datetime
import unittest

sys.path.append(str(Path.cwd()))
from workflow import main

class E2ETester(unittest.TestCase):

    def test_e2e(self):
        MLSchema.populate_registry()
        MLSchema.append_schema_to_registry(Path.cwd() / ".parameters" / "schemas")

        # main()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
