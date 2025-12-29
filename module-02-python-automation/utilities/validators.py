import jsonschema
from jsonschema import validate

def validate_json_schema(data, schema):
    """Validate data against JSON schema"""
    try:
        validate(instance=data, schema=schema)
        return True, "Valid"
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)