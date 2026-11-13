"""Sample app: stores the note text in S3 and its metadata in DynamoDB."""
import boto3


class NotesRepository:
    def __init__(self, bucket: str, table: str):
        self.bucket = bucket
        self.table = table
        # No endpoint or credentials in the code: the SDK reads the environment variables.
        self.s3 = boto3.client("s3")
        self.dynamodb = boto3.client("dynamodb")

    def save(self, note_id: str, text: str) -> None:
        body = text.encode("utf-8")
        key = f"notes/{note_id}.txt"
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=body)
        self.dynamodb.put_item(
            TableName=self.table,
            Item={
                "id": {"S": note_id},
                "s3_key": {"S": key},
                "size": {"N": str(len(body))},
            },
        )

    def load(self, note_id: str) -> str | None:
        item = self.dynamodb.get_item(
            TableName=self.table, Key={"id": {"S": note_id}}
        ).get("Item")
        if item is None:
            return None
        obj = self.s3.get_object(Bucket=self.bucket, Key=item["s3_key"]["S"])
        return obj["Body"].read().decode("utf-8")
