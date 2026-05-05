import json
import boto3
import os
from botocore.exceptions import ClientError


class S3Repository:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket = os.environ.get("DATABASE_BUCKET")
        self.key = os.environ.get("DATABASE_KEY", "doctors.json")

        if not self.bucket:
            raise ValueError("DATABASE_BUCKET environment variable is required")

    def read(self):
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=self.key)
            return json.loads(obj["Body"].read())

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return []
            raise  # rethrow other errors

    def write(self, data):
        self.s3.put_object(
            Bucket=self.bucket,
            Key=self.key,
            Body=json.dumps(data)
        )