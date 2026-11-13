import os
import sys
import uuid
from pathlib import Path

import boto3
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notes_app import NotesRepository  # noqa: E402

EMULATOR_ACCOUNT = "000000000000"


@pytest.fixture(scope="session", autouse=True)
def only_against_the_emulator():
    """Safety guard: abort if the tests are not talking to the emulator."""
    endpoint = os.environ.get("AWS_ENDPOINT_URL", "")
    if not endpoint.startswith("https://127.0.0.1"):
        pytest.exit(
            "AWS_ENDPOINT_URL does not point at the local emulator. Run: source emulator-env.sh",
            returncode=1,
        )
    account = boto3.client("sts").get_caller_identity()["Account"]
    if account != EMULATOR_ACCOUNT:
        pytest.exit(
            f"Account {account} is not the emulator account. Aborting so real AWS is never touched.",
            returncode=1,
        )


@pytest.fixture
def repo():
    """Creates a fresh bucket and table for each test."""
    suffix = uuid.uuid4().hex[:8]
    bucket = f"notes-{suffix}"
    table = f"notes-{suffix}"

    boto3.client("s3").create_bucket(Bucket=bucket)

    dynamodb = boto3.client("dynamodb")
    dynamodb.create_table(
        TableName=table,
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        BillingMode="PAY_PER_REQUEST",
    )
    dynamodb.get_waiter("table_exists").wait(TableName=table)

    return NotesRepository(bucket, table)
