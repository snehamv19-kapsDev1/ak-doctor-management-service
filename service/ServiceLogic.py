import uuid
import logging
from Validation import validate_create, validate_update
from Response import response

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_doctors(repo):
    logger.info("Retrieving all doctors")
    doctors = repo.read()
    logger.info(f"Found {len(doctors)} doctors")
    return response(200, doctors)


def get_doctor_by_id(repo, doctor_id):
    logger.info(f"Searching for doctor with ID: {doctor_id}")
    doctors = repo.read()

    for d in doctors:
        if d["id"] == doctor_id:
            logger.info(f"Doctor found: {d['name']}")
            return response(200, d)

    logger.warning(f"Doctor not found with ID: {doctor_id}")
    return response(404, {"message": "Doctor not found"})


def create_doctor(repo, body):
    logger.info("Creating new doctor")
    errors = validate_create(body)
    if errors:
        logger.warning(f"Validation failed for doctor creation: {errors}")
        return response(400, {"errors": errors})

    data = repo.read()

    new_doc = {
        "id": str(uuid.uuid4()),
        "name": body["name"].strip(),
        "specialization": body["specialization"].strip()
    }

    data.append(new_doc)
    repo.write(data)

    logger.info(f"Doctor created successfully with ID: {new_doc['id']}")
    return response(201, new_doc)


def update_doctor(repo, doctor_id, body):
    logger.info(f"Updating doctor with ID: {doctor_id}")
    data = repo.read()

    for d in data:
        if d["id"] == doctor_id:
            errors = validate_update(body)
            if errors:
                logger.warning(f"Validation failed for doctor update: {errors}")
                return response(400, {"errors": errors})

            original_name = d["name"]
            original_specialization = d["specialization"]

            if "name" in body:
                d["name"] = body["name"]
                logger.info(f"Updated name from '{original_name}' to '{d['name']}'")

            if "specialization" in body:
                d["specialization"] = body["specialization"]
                logger.info(f"Updated specialization from '{original_specialization}' to '{d['specialization']}'")

            repo.write(data)
            logger.info(f"Doctor updated successfully: {doctor_id}")
            return response(200, d)

    logger.warning(f"Doctor not found for update with ID: {doctor_id}")
    return response(404, {"message": "Doctor not found"})


def delete_doctor(repo, doctor_id):
    logger.info(f"Deleting doctor with ID: {doctor_id}")
    data = repo.read()

    new_data = [d for d in data if d["id"] != doctor_id]

    if len(new_data) == len(data):
        logger.warning(f"Doctor not found for deletion with ID: {doctor_id}")
        return response(404, {"message": "Doctor not found"})

    repo.write(new_data)
    logger.info(f"Doctor deleted successfully: {doctor_id}")
    return response(200, {"message": "Deleted"})