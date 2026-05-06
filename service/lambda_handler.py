import json
import logging
from repository import S3Repository
from ServiceLogic import *
from Response import response

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    repo = S3Repository()  # REAL dependency

    try:
        method = event.get("httpMethod")
        path = event.get("path")
        body = json.loads(event.get("body") or "{}")
        path_params = event.get("pathParameters") or {}
        doctor_id = path_params.get("id")

        logger.info(f"Processing request: {method} {path}")

        if method == "GET" and path == "/doctors":
            logger.info("Getting all doctors")
            return get_all_doctors(repo)

        if method == "GET" and doctor_id:
            logger.info(f"Getting doctor by ID: {doctor_id}")
            return get_doctor_by_id(repo, doctor_id)

        if method == "POST":
            logger.info("Creating new doctor")
            return create_doctor(repo, body)

        if method == "PUT" and doctor_id:
            logger.info(f"Updating doctor: {doctor_id}")
            return update_doctor(repo, doctor_id, body)

        if method == "DELETE" and doctor_id:
            logger.info(f"Deleting doctor: {doctor_id}")
            return delete_doctor(repo, doctor_id)

        logger.warning(f"Route not found: {method} {path}")
        return response(404, {"message": "Routes not found"})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return response(500, {"error": str(e)})
