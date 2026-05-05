from ..Validation import validate_create, validate_update

def test_validate_create_success():
    body = {"name": "Dr A", "specialization": "Cardiology"}
    assert validate_create(body) == []


def test_validate_create_missing_fields():
    body = {}
    errors = validate_create(body)

    assert "name is required" in errors
    assert "specialization is required" in errors


def test_validate_update_empty_value():
    body = {"name": ""}
    errors = validate_update(body)

    assert "name cannot be empty" in errors