import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_create(body):
    logger.info("Validating doctor creation request")
    errors = []

    if not body:
        errors.append("request body required")

    if not body.get("name"):
        errors.append("name is required")

    if not body.get("specialization"):
        errors.append("specialization is required")

    if errors:
        logger.warning(f"Validation failed for create: {errors}")
    else:
        logger.info("Validation passed for create")

    return errors


def validate_update(body):
    logger.info("Validating doctor update request")
    errors = []

    if not body:
        logger.warning("Empty request body for update")
        return ["request body required"]

    if "name" in body and not body["name"]:
        errors.append("name cannot be empty")

    if "specialization" in body and not body["specialization"]:
        errors.append("specialization cannot be empty")

    if errors:
        logger.warning(f"Validation failed for update: {errors}")
    else:
        logger.info("Validation passed for update")

    return errors