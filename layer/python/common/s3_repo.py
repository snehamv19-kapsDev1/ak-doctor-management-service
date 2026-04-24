import json
import os

FILE = "/tmp/doctors.json"

def read_all_with_etag():
    try:
        if not os.path.exists(FILE):
            return [], None

        with open(FILE, "r") as f:
            return json.load(f), None
    except:
        return [], None

def write_all(rows, etag=None):
    with open(FILE, "w") as f:
        json.dump(rows, f, indent=2)

def get_by_id(doc_id):
    rows, _ = read_all_with_etag()
    for r in rows:
        if r["id"] == str(doc_id):
            return r
    return None