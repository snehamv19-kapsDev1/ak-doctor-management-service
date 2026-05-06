import json
import boto3
import os
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class S3Repository:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket = os.environ.get("DATABASE_BUCKET")
        self.key = os.environ.get("DATABASE_KEY", "doctors.json")

        if not self.bucket:
            logger.error("DATABASE_BUCKET environment variable is required")
            raise ValueError("DATABASE_BUCKET environment variable is required")

        logger.info(f"S3Repository initialized with bucket: {self.bucket}, key: {self.key}")

    def read(self):
        try:
            logger.info(f"Reading data from S3: {self.bucket}/{self.key}")
            obj = self.s3.get_object(Bucket=self.bucket, Key=self.key)
            data = json.loads(obj["Body"].read())
            logger.info(f"Successfully read {len(data)} records from S3")
            return data

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.info(f"S3 key does not exist, returning empty list: {self.bucket}/{self.key}")
                return []
            logger.error(f"S3 read error: {e}")
            raise  # rethrow other errors

    def write(self, data):
        try:
            logger.info(f"Writing {len(data)} records to S3: {self.bucket}/{self.key}")
            self.s3.put_object(
                Bucket=self.bucket,
                Key=self.key,
                Body=json.dumps(data)
            )
            logger.info("Successfully wrote data to S3")
        except ClientError as e:
            logger.error(f"S3 write error: {e}")
            raise
