import json
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def response(status, body):
    logger.info(f"Creating response with status: {status}")
    response_obj = {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
    logger.debug(f"Response body: {response_obj['body']}")
    return response_obj
