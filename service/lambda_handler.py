import traceback

#
#
#
import json
import logging
# from repository import S3Repository
# from ServiceLogic import *
from Response import response

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Common CORS headers
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",  # change to frontend URL in prod
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
}

def add_cors_headers(res):
    """
    Add CORS headers to every response
    """
    if "headers" not in res:
        res["headers"] = {}

    res["headers"].update(CORS_HEADERS)
    return res
def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")  # Log incoming event

    try:
        response(200, {"message": "Hello from Lambda!"})
    except Exception as e:
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Exception message: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return add_cors_headers(response(500, {"error": str(e)}))




#
# def lambda_handler(event, context):
#     repo = S3Repository()  # REAL dependency
#
#     try:
#         method = event.get("httpMethod")
#         path = event.get("path")
#         body = json.loads(event.get("body") or "{}")
#         path_params = event.get("pathParameters") or {}
#         doctor_id = path_params.get("id")
#
#         logger.info(f"Processing request: {method} {path}")
#
#         # Handle preflight CORS request
#         if method == "OPTIONS":
#             return {
#                 "statusCode": 200,
#                 "headers": CORS_HEADERS,
#                 "body": json.dumps({"message": "CORS preflight success"})
#             }
#
#         if method == "GET" and path == "/doctors":
#             logger.info("Getting all doctors")
#             return add_cors_headers(get_all_doctors(repo))
#
#         if method == "GET" and doctor_id:
#             logger.info(f"Getting doctor by ID: {doctor_id}")
#             return add_cors_headers(get_doctor_by_id(repo, doctor_id))
#
#         if method == "POST":
#             logger.info("Creating new doctor")
#             return add_cors_headers(create_doctor(repo, body))
#
#         if method == "PUT" and doctor_id:
#             logger.info(f"Updating doctor: {doctor_id}")
#             return add_cors_headers(update_doctor(repo, doctor_id, body))
#
#         if method == "DELETE" and doctor_id:
#             logger.info(f"Deleting doctor: {doctor_id}")
#             return add_cors_headers(delete_doctor(repo, doctor_id))
#
#         logger.warning(f"Route not found: {method} {path}")
#         return add_cors_headers(
#             response(404, {"message": "Routes not found"})
#         )
#
#     except Exception as e:
#         logger.error(f"Error processing request: {str(e)}")
#
#         return add_cors_headers(
#             response(500, {"error": str(e)})
#         )