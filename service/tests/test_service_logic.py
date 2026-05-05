import json
import os
import boto3
from moto import mock_aws
from service.lambda_handler import lambda_handler


@mock_aws
def test_lambda_post_create():
    # Setup environment
    os.environ["DATABASE_BUCKET"] = "test-bucket"
    os.environ["DATABASE_KEY"] = "doctors.json"
    
    # Create S3 bucket for testing
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    
    event = {
        "httpMethod": "POST",
        "path": "/doctors",
        "body": json.dumps({
            "name": "Dr A",
            "specialization": "Cardiology"
        }),
        "pathParameters": None
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 201  # Should be 201 for creation
    
    # Clean up
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_lambda_route_not_found():
    # Setup environment
    os.environ["DATABASE_BUCKET"] = "test-bucket"
    os.environ["DATABASE_KEY"] = "doctors.json"
    
    # Create S3 bucket for testing
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    
    event = {
        "httpMethod": "GET",
        "path": "/invalid",
        "body": None,
        "pathParameters": None
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 404
    
    # Clean up
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_lambda_get_all():
    # Setup environment
    os.environ["DATABASE_BUCKET"] = "test-bucket"
    os.environ["DATABASE_KEY"] = "doctors.json"
    
    # Create S3 bucket for testing
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    
    event = {
        "httpMethod": "GET",
        "path": "/doctors",
        "body": None,
        "pathParameters": None
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    
    # Clean up
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]
