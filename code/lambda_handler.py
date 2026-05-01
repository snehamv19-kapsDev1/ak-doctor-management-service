import json
from service_logic import create_doctor, get_all_doctors

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "LAMBDA EXECUTED SUCCESSFULLY dfasf ",
            "event": event
        })
    }
    # try:
    #     http_method = event.get("httpMethod")
    #     path = event.get("path")
    #
    #     if http_method == "POST" and path.endswith("/item"):
    #         body = json.loads(event.get("body", "{}"))
    #         return create_doctor(body)
    #
    #     elif http_method == "GET" and path.endswith("/items"):
    #         return get_all_doctors()
    #
    #     else:
    #         return response(404, {"message": "Route not found"})
    #
    # except Exception as e:
    #     return response(500, {"error": str(e)})


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }