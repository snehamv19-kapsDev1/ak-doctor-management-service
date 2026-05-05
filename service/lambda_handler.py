import json
from service.repository import S3Repository
from service.ServiceLogic import *
from service.Response import response


def lambda_handler(event, context):
    repo = S3Repository()  # REAL dependency

    try:
        method = event.get("httpMethod")
        path = event.get("path")
        body = json.loads(event.get("body") or "{}")
        path_params = event.get("pathParameters") or {}
        doctor_id = path_params.get("id")

        if method == "GET" and path == "/doctors":
            return get_all_doctors(repo)

        if method == "GET" and doctor_id:
            return get_doctor_by_id(repo, doctor_id)

        if method == "POST":
            return create_doctor(repo, body)

        if method == "PUT" and doctor_id:
            return update_doctor(repo, doctor_id, body)

        if method == "DELETE" and doctor_id:
            return delete_doctor(repo, doctor_id)

        return response(404, {"message": "Routes not found"})

    except Exception as e:
        return response(500, {"error": str(e)})