import json
import os
import uuid
import boto3
import pytest
from moto import mock_aws
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ..lambda_handler import lambda_handler

# Load test constants
with open(os.path.join(os.path.dirname(__file__), 'tests_constants.json'), 'r') as f:
    CONSTANTS = json.load(f)


@mock_aws
def test_lambda_post_create():
    # Setup environment
    os.environ["DATABASE_BUCKET"] = CONSTANTS['DATABASE_BUCKET']
    os.environ["DATABASE_KEY"] = CONSTANTS['DATABASE_KEY']

    # Create S3 bucket for testing
    s3 = boto3.client("s3", region_name=CONSTANTS['AWS_REGION'])
    s3.create_bucket(Bucket=CONSTANTS['DATABASE_BUCKET'])
    
    event = {
        "httpMethod": CONSTANTS['HTTP_METHODS']['POST'],
        "path": "/doctors",
        "body": json.dumps(CONSTANTS['TEST_DATA']['new_doctor']),
        "pathParameters": None
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == CONSTANTS['HTTP_STATUS']['CREATED']
    
    # Clean up
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_lambda_route_not_found():
    # Setup environment
    os.environ["DATABASE_BUCKET"] = CONSTANTS['DATABASE_BUCKET']
    os.environ["DATABASE_KEY"] = CONSTANTS['DATABASE_KEY']
    
    # Create S3 bucket for testing
    s3 = boto3.client("s3", region_name=CONSTANTS['AWS_REGION'])
    s3.create_bucket(Bucket=CONSTANTS['DATABASE_BUCKET'])
    
    event = {
        "httpMethod": CONSTANTS['HTTP_METHODS']['GET'],
        "path": "/invalid",
        "body": None,
        "pathParameters": None
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == CONSTANTS['HTTP_STATUS']['NOT_FOUND']
    
    # Clean up
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]


@mock_aws
def test_lambda_get_all():
    # Setup environment
    os.environ["DATABASE_BUCKET"] = CONSTANTS['DATABASE_BUCKET']
    os.environ["DATABASE_KEY"] = CONSTANTS['DATABASE_KEY']
    
    # Create S3 bucket for testing
    s3 = boto3.client("s3", region_name=CONSTANTS['AWS_REGION'])
    s3.create_bucket(Bucket=CONSTANTS['DATABASE_BUCKET'])
    
    event = {
        "httpMethod": CONSTANTS['HTTP_METHODS']['GET'],
        "path": "/doctors",
        "body": None,
        "pathParameters": None
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == CONSTANTS['HTTP_STATUS']['OK']
    
    # Clean up
    del os.environ["DATABASE_BUCKET"]
    del os.environ["DATABASE_KEY"]
