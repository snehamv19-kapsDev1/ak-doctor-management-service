import json
import os
import uuid
import boto3
import pytest
from moto import mock_aws
from service.lambda_handler import lambda_handler


@pytest.fixture(autouse=True)
def setup_env():
    bucket_name = f"test-bucket-{uuid.uuid4().hex[:8]}"
    os.environ["DATABASE_BUCKET"] = bucket_name
    os.environ["DATABASE_KEY"] = "doctors.json"
    return bucket_name


@mock_aws
def test_get_all_doctors_empty(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "GET",
        "path": "/doctors",
        "body": None,
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == []


@mock_aws
def test_get_all_doctors_with_data(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    initial_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"},
        {"id": "2", "name": "Dr. Johnson", "specialization": "Neurology"}
    ]
    s3.put_object(Bucket=bucket_name, Key="doctors.json", Body=json.dumps(initial_data))

    event = {
        "httpMethod": "GET",
        "path": "/doctors",
        "body": None,
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == initial_data


@mock_aws
def test_get_doctor_by_id_found(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    initial_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"},
        {"id": "2", "name": "Dr. Johnson", "specialization": "Neurology"}
    ]
    s3.put_object(Bucket=bucket_name, Key="doctors.json", Body=json.dumps(initial_data))

    event = {
        "httpMethod": "GET",
        "path": "/doctors/1",
        "body": None,
        "pathParameters": {"id": "1"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == initial_data[0]


@mock_aws
def test_get_doctor_by_id_not_found(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "GET",
        "path": "/doctors/999",
        "body": None,
        "pathParameters": {"id": "999"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 404
    assert json.loads(res["body"]) == {"message": "Doctor not found"}


@mock_aws
def test_create_doctor_valid(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "POST",
        "path": "/doctors",
        "body": json.dumps({
            "name": "Dr. Brown",
            "specialization": "Dermatology"
        }),
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 201
    body = json.loads(res["body"])
    assert body["name"] == "Dr. Brown"
    assert body["specialization"] == "Dermatology"
    assert "id" in body


@mock_aws
def test_create_doctor_invalid_missing_name(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "POST",
        "path": "/doctors",
        "body": json.dumps({
            "specialization": "Dermatology"
        }),
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 400
    assert "name is required" in json.loads(res["body"])["errors"]


@mock_aws
def test_create_doctor_invalid_missing_specialization(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "POST",
        "path": "/doctors",
        "body": json.dumps({
            "name": "Dr. Brown"
        }),
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 400
    assert "specialization is required" in json.loads(res["body"])["errors"]


@mock_aws
def test_create_doctor_invalid_empty_body(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "POST",
        "path": "/doctors",
        "body": json.dumps({}),
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 400
    errors = json.loads(res["body"])["errors"]
    assert "request body required" in errors


@mock_aws
def test_update_doctor_valid(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    initial_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"}
    ]
    s3.put_object(Bucket=bucket_name, Key="doctors.json", Body=json.dumps(initial_data))

    event = {
        "httpMethod": "PUT",
        "path": "/doctors/1",
        "body": json.dumps({
            "name": "Dr. Smith Updated",
            "specialization": "Cardiology Updated"
        }),
        "pathParameters": {"id": "1"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    body = json.loads(res["body"])
    assert body["name"] == "Dr. Smith Updated"
    assert body["specialization"] == "Cardiology Updated"


@mock_aws
def test_update_doctor_partial_update_name(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    initial_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"}
    ]
    s3.put_object(Bucket=bucket_name, Key="doctors.json", Body=json.dumps(initial_data))

    event = {
        "httpMethod": "PUT",
        "path": "/doctors/1",
        "body": json.dumps({
            "name": "Dr. Smith Updated"
        }),
        "pathParameters": {"id": "1"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    body = json.loads(res["body"])
    assert body["name"] == "Dr. Smith Updated"
    assert body["specialization"] == "Cardiology"


@mock_aws
def test_update_doctor_invalid_empty_name(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    initial_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"}
    ]
    s3.put_object(Bucket=bucket_name, Key="doctors.json", Body=json.dumps(initial_data))

    event = {
        "httpMethod": "PUT",
        "path": "/doctors/1",
        "body": json.dumps({
            "name": ""
        }),
        "pathParameters": {"id": "1"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 400
    assert "name cannot be empty" in json.loads(res["body"])["errors"]


@mock_aws
def test_update_doctor_not_found(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "PUT",
        "path": "/doctors/999",
        "body": json.dumps({
            "name": "Dr. New"
        }),
        "pathParameters": {"id": "999"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 404
    assert json.loads(res["body"]) == {"message": "Doctor not found"}


@mock_aws
def test_delete_doctor_found(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    initial_data = [
        {"id": "1", "name": "Dr. Smith", "specialization": "Cardiology"},
        {"id": "2", "name": "Dr. Johnson", "specialization": "Neurology"}
    ]
    s3.put_object(Bucket=bucket_name, Key="doctors.json", Body=json.dumps(initial_data))

    event = {
        "httpMethod": "DELETE",
        "path": "/doctors/1",
        "body": None,
        "pathParameters": {"id": "1"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == {"message": "Deleted"}

    # Verify deletion
    get_event = {
        "httpMethod": "GET",
        "path": "/doctors",
        "body": None,
        "pathParameters": None
    }
    get_res = lambda_handler(get_event, None)
    remaining_doctors = json.loads(get_res["body"])
    assert len(remaining_doctors) == 1
    assert remaining_doctors[0]["id"] == "2"


@mock_aws
def test_delete_doctor_not_found(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "DELETE",
        "path": "/doctors/999",
        "body": None,
        "pathParameters": {"id": "999"}
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 404
    assert json.loads(res["body"]) == {"message": "Doctor not found"}


@mock_aws
def test_route_not_found(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "GET",
        "path": "/invalid",
        "body": None,
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 404
    assert json.loads(res["body"]) == {"message": "Route not found"}


@mock_aws
def test_invalid_json_body(setup_env):
    bucket_name = setup_env
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    event = {
        "httpMethod": "POST",
        "path": "/doctors",
        "body": "invalid json",
        "pathParameters": None
    }
    res = lambda_handler(event, None)
    assert res["statusCode"] == 500
    assert "error" in json.loads(res["body"])
