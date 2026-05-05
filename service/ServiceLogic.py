import uuid
from service.Validation import validate_create, validate_update
from service.Response import response


def get_all_doctors(repo):
    return response(200, repo.read())


def get_doctor_by_id(repo, doctor_id):
    for d in repo.read():
        if d["id"] == doctor_id:
            return response(200, d)

    return response(404, {"message": "Doctor not found"})


def create_doctor(repo, body):
    errors = validate_create(body)
    if errors:
        return response(400, {"errors": errors})

    data = repo.read()

    new_doc = {
        "id": str(uuid.uuid4()),
        "name": body["name"].strip(),
        "specialization": body["specialization"].strip()
    }

    data.append(new_doc)
    repo.write(data)

    return response(201, new_doc)


def update_doctor(repo, doctor_id, body):
    data = repo.read()

    for d in data:
        if d["id"] == doctor_id:

            errors = validate_update(body)
            if errors:
                return response(400, {"errors": errors})

            if "name" in body:
                d["name"] = body["name"]

            if "specialization" in body:
                d["specialization"] = body["specialization"]

            repo.write(data)
            return response(200, d)

    return response(404, {"message": "Doctor not found"})


def delete_doctor(repo, doctor_id):
    data = repo.read()

    new_data = [d for d in data if d["id"] != doctor_id]

    if len(new_data) == len(data):
        return response(404, {"message": "Doctor not found"})

    repo.write(new_data)
    return response(200, {"message": "Deleted"})