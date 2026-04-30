# import json
# from common.s3_repo import read_all_with_etag, write_all
# from common.utils import response, log_info, log_error, retry_with_backoff
#
# def handler(event, context):
#     try:
#         doc_id = str(event["pathParameters"]["id"])
#         body = json.loads(event["body"])
#
#         def operation():
#             rows, etag = read_all_with_etag()
#
#             for i, r in enumerate(rows):
#                 if r["id"] == doc_id:
#                     body.pop("id", None)  # prevent id overwrite
#                     rows[i].update(body)
#
#                     write_all(rows, etag)
#
#                     return response(200, rows[i])
#
#             return response(404, {"error": "Doctor not found"})
#
#         result = retry_with_backoff(operation)
#
#         log_info("Doctor updated", doctorId=doc_id)
#         return result
#
#     except Exception as e:
#         log_error("Update failed", error=str(e))
#         return response(500, {"error": "Internal server error"})