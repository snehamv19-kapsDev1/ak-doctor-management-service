import json
import os
import boto3
import pytest
from moto import mock_aws
from ..repository import S3Repository


@mock_aws
def test_repository_read_empty():
    """Test reading from an empty/non-existent S3 object"""
    # Setup
    bucket_name = "test-bucket"
    key = "doctors.json"
    os.environ["DATABASE_BUCKET"] = bucket_name
    os.environ["DATABASE_KEY"] = key

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    # Test
    repo = S3Repository()
    data = repo.read()

    assert data == []

    # Cleanup
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_repository_read_with_data():
    """Test reading from S3 object with existing data"""
    # Setup
    bucket_name = "test-bucket"
    key = "doctors.json"
    os.environ["DATABASE_BUCKET"] = bucket_name
    os.environ["DATABASE_KEY"] = key

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    test_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"},
        {"id": "2", "name": "Dr. Johnson", "specialization": "Neurology"}
    ]
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(test_data))

    # Test
    repo = S3Repository()
    data = repo.read()

    assert data == test_data

    # Cleanup
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_repository_write():
    """Test writing data to S3"""
    # Setup
    bucket_name = "test-bucket"
    key = "doctors.json"
    os.environ["DATABASE_BUCKET"] = bucket_name
    os.environ["DATABASE_KEY"] = key

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    # Test
    repo = S3Repository()
    test_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"}
    ]
    repo.write(test_data)

    # Verify
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    stored_data = json.loads(obj["Body"].read())
    assert stored_data == test_data

    # Cleanup
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_repository_init_missing_bucket():
    """Test that repository raises error when DATABASE_BUCKET is not set"""
    if "DATABASE_BUCKET" in os.environ:
        del os.environ["DATABASE_BUCKET"]

    with pytest.raises(ValueError, match="DATABASE_BUCKET environment variable is required"):
        S3Repository()


@mock_aws
def test_repository_round_trip():
    """Test reading and writing data in sequence"""
    # Setup
    bucket_name = "test-bucket"
    key = "doctors.json"
    os.environ["DATABASE_BUCKET"] = bucket_name
    os.environ["DATABASE_KEY"] = key

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    # Test
    repo = S3Repository()

    # Initially empty
    assert repo.read() == []

    # Write data
    test_data = [{"id": "1", "name": "Dr. Test", "specialization": "Testology"}]
    repo.write(test_data)

    # Read back
    assert repo.read() == test_data

    # Write more data
    updated_data = [
        {"id": "1", "name": "Dr. Test", "specialization": "Testology"},
        {"id": "2", "name": "Dr. Updated", "specialization": "Updatedology"}
    ]
    repo.write(updated_data)

    # Read back updated data
    assert repo.read() == updated_data

    # Cleanup
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]
