# from common.s3_repo import read_all_with_etag, write_all
# from common.utils import response, log_info, log_error, retry_with_backoff
#
#
# def handler(event, context):
#     try:
#         doc_id = str(event["pathParameters"]["id"])
#
#         def operation():
#             rows, etag = read_all_with_etag()
#
#             new_rows = [r for r in rows if r["id"] != doc_id]
#
#             if len(rows) == len(new_rows):
#                 return response(404, {"error": "Doctor not found"})
#
#             write_all(new_rows, etag)
#
#             return response(200, {"message": "Doctor deleted"})
#
#         result = retry_with_backoff(operation)
#
#         log_info("Doctor deleted", doctorId=doc_id)
#         return result
#
#     except Exception as e:
#         log_error("Delete failed", error=str(e))
#         return response(500, {"error": "Internal server error"})