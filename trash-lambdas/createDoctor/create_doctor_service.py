# from common.s3_repo import read_all_with_etag, write_all
#
#
# def create_doctors(data):
#     rows, etag = read_all_with_etag()
#
#     # ---------------- BULK ----------------
#     if isinstance(data, list):
#         added = []
#
#         for item in data:
#             if not isinstance(item, dict):
#                 continue
#
#             if "id" not in item:
#                 continue
#
#             item_id = str(item["id"])
#             item["id"] = item_id
#
#             if any(str(r.get("id")) == item_id for r in rows):
#                 continue
#
#             rows.append(item)
#             added.append(item)
#
#         write_all(rows, etag)
#
#         return {
#             "message": "bulk inserted",
#             "added": len(added)
#         }
#
#     # ---------------- SINGLE ----------------
#     if isinstance(data, dict):
#         body_id = str(data["id"])
#         data["id"] = body_id
#
#         if any(str(r.get("id")) == body_id for r in rows):
#             return {"error": "exists"}
#
#         rows.append(data)
#         write_all(rows, etag)
#
#         return data
#
#     return {"error": "invalid format"}