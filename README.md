# AWS Emulator notes demo

A small Python app that stores a note's text in Amazon S3 and its metadata in Amazon DynamoDB, tested with pytest against [AWS Emulator](https://aws.amazon.com/blogs/aws/test-your-applications-against-aws-locally-with-aws-emulator/) (launched by AWS on November 11, 2026). No AWS account and no cost.

This is the companion code for the article **AWS Emulator in practice: test AWS on your machine, with no account and no cost**.

## What is inside

| File | What it does |
| --- | --- |
| `notes_app.py` | The app. No endpoint or credentials in the code: the SDK reads environment variables. |
| `emulator-env.sh` | Points the AWS CLI and SDKs at the local emulator. |
| `tests/conftest.py` | Safety guard (aborts if not talking to the emulator) and a fresh bucket and table per test. |
| `tests/test_notes.py` | Four tests: save and load, missing note, Unicode, overwrite. |
| `.github/workflows/tests.yml` | Installs the emulator on GitHub Actions and runs the tests, with no AWS secrets. |

## Run it locally

1. Install and start AWS Emulator (Linux shown; macOS and Windows use Docker, see the article):

   ```bash
   aws-emulator --telemetry off
   ```

2. In a second terminal:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   source emulator-env.sh
   aws sts get-caller-identity   # Account must be 000000000000
   pytest -q tests               # 4 passed
   ```

## Limitations

AWS Emulator does not evaluate IAM policies the way AWS does, and each emulator is a single account. Test permissions on real AWS. See the [AWS Emulator User Guide](https://docs.aws.amazon.com/emulator/latest/userguide/what-is-service.html).

## Author

Guilherme Benfica · AWS Golden Jacket
