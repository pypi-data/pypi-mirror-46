"""Settings and variables for TOS."""
import json
import os
import platform

DIRNAME = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.abspath(os.path.join(DIRNAME, os.pardir))
PLATFORM = platform.system()

#:
DEFAULT_DB_ADDRESS = "mongodb://localhost:27017/"

# Items are given "new" status when the producer creates them
# When the consumers check out the item, its status will
# be set as "processing". When the consumer finishes, the
# status will be set "pass" or "fail" depending on the outcome.
# when case for manual intervention is detected, the status
# will be set to "expected_fail".

#:
VALID_STATUSES = [
    "new",
    "processing",
    "pass",
    "fail",
    "expected_fail",  # manual handling
]

with open(os.path.join(DIRNAME, "schema.json"), "r") as f:
    schema = json.load(f)

VALIDATOR = {"validator": schema}
