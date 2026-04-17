from common.s3_repo import read_all_with_etag
from common.utils import response, log_info, log_error


def handler(event, context):
    try:
        doc_id = str(event["pathParameters"]["id"])

        rows, _ = read_all_with_etag()

        for r in rows:
            if r["id"] == doc_id:
                log_info("Doctor fetched", doctorId=doc_id)
                return response(200, r)

        return response(404, {"error": "Doctor not found"})

    except Exception as e:
        log_error("Get failed", error=str(e))
        return response(500, {"error": "Internal server error"})