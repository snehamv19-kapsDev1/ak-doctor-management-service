from flask import Flask, request, jsonify
from lambdas.createDoctor.create_doctor_service import create_doctors
from db_utils.s3_repo import read_all_with_etag

app = Flask(__name__)


@app.route("/doctors", methods=["POST"])
def create():
    body = request.get_json(silent=True)

    if not body:
        return jsonify({"error": "Invalid JSON"}), 400

    result = create_doctors(body)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@app.route("/doctors", methods=["GET"])
def get_all():
    rows, _ = read_all_with_etag()
    return jsonify(rows)


@app.route("/doctors/<id>", methods=["GET"])
def get_one(id):
    rows, _ = read_all_with_etag()

    for r in rows:
        if str(r["id"]) == str(id):
            return jsonify(r)

    return jsonify({"error": "not found"}), 404


@app.route("/doctors/<id>", methods=["PUT"])
def update(id):
    from common.s3_repo import read_all_with_etag, write_all

    body = request.get_json(silent=True)
    rows, etag = read_all_with_etag()

    for i, r in enumerate(rows):
        if str(r["id"]) == str(id):
            body.pop("id", None)
            rows[i].update(body)
            write_all(rows, etag)
            return jsonify(rows[i])

    return jsonify({"error": "not found"}), 404


@app.route("/doctors/<id>", methods=["DELETE"])
def delete(id):
    from common.s3_repo import read_all_with_etag, write_all

    rows, etag = read_all_with_etag()

    new_rows = [r for r in rows if str(r["id"]) != str(id)]

    if len(new_rows) == len(rows):
        return jsonify({"error": "not found"}), 404

    write_all(new_rows, etag)

    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    app.run(port=3000, debug=True)