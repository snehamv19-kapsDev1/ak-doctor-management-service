def validate_create(body):
    errors = []

    if not body:
        errors.append("request body required")

    if not body.get("name"):
        errors.append("name is required")

    if not body.get("specialization"):
        errors.append("specialization is required")

    return errors


def validate_update(body):
    errors = []

    if not body:
        return ["request body required"]

    if "name" in body and not body["name"]:
        errors.append("name cannot be empty")

    if "specialization" in body and not body["specialization"]:
        errors.append("specialization cannot be empty")

    return errors