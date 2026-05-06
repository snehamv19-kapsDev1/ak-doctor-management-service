import pytest
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ..Validation import validate_create, validate_update

# Load test constants
with open(os.path.join(os.path.dirname(__file__), 'tests_constants.json'), 'r') as f:
    CONSTANTS = json.load(f)

def test_validate_create_success():
    body = CONSTANTS['TEST_DATA']['new_doctor']
    assert validate_create(body) == []


def test_validate_create_missing_fields():
    body = {}
    errors = validate_create(body)

    assert CONSTANTS['ERROR_MESSAGES']['NAME_REQUIRED'] in errors
    assert CONSTANTS['ERROR_MESSAGES']['SPECIALIZATION_REQUIRED'] in errors


def test_validate_update_empty_value():
    body = {"name": ""}
    errors = validate_update(body)

    assert CONSTANTS['ERROR_MESSAGES']['NAME_CANNOT_BE_EMPTY'] in errors
