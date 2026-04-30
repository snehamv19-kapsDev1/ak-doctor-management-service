import json
import boto3
import os
import uuid

s3 = boto3.client("s3")

BUCKET = os.environ.get("BUCKET")
KEY = "doctors.json"


def get_all_doctors():
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=KEY)
        data = json.loads(obj["Body"].read())
    except s3.exceptions.NoSuchKey:
        data = []

    return response(200, data)


def create_doctor(body):
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=KEY)
        data = json.loads(obj["Body"].read())
    except s3.exceptions.NoSuchKey:
        data = []

    new_doctor = {
        "id": str(uuid.uuid4()),
        "name": body.get("name"),
        "specialization": body.get("specialization")
    }

    data.append(new_doctor)

    s3.put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=json.dumps(data)
    )

    return response(201, new_doctor)


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }