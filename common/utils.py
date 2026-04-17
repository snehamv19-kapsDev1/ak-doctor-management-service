import json
import logging
import time
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


def log_info(message, **kwargs):
    logger.info(json.dumps({"message": message, **kwargs}))


def log_error(message, **kwargs):
    logger.error(json.dumps({"message": message, **kwargs}))


# 🔁 retry helper
def retry_with_backoff(fn, retries=3):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if attempt == retries - 1:
                raise e
            sleep = (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(sleep)