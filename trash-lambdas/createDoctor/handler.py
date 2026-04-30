# import json
# from common.utils import response
# from create_doctor_service import create_doctors
#
#
# def handler(event, context):
#     try:
#         body = json.loads(event.get("body") or "[]")
#
#         result = create_doctors(body)
#
#         if "error" in result:
#             return response(400, result)
#
#         return response(201, result)
#
#     except Exception as e:
#         return response(500, {"error": str(e)})