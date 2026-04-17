from common.s3_repo import read_all_with_etag
from common.utils import response

def handler(event, context):
    rows, _ = read_all_with_etag()
    return response(200, rows)