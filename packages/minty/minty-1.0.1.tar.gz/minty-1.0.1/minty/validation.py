import json
from functools import wraps
from uuid import UUID

import statsd
from jsonpointer import JsonPointer
from jsonschema import Draft7Validator, draft7_format_checker

from .exceptions import ValidationError

_format_checker = draft7_format_checker


@_format_checker.checks("uuid", raises=ValueError)
def is_uuid(instance):
    return UUID(hex=instance)


def validate_with(schema_data: bytes):
    """Ensure the decorated function is called with valid arguments

    :param schema_data: The JSONSchema to validate against.
        Should be UTF-8-encoded JSON bytes.
    :type schema_data: bytes
    :return: Decorator for validating function arguments against `schema`
    """
    schema = json.loads(schema_data.decode("utf-8"))

    def validity_wrapper(f):
        validator = Draft7Validator(
            schema=schema, format_checker=_format_checker
        )

        @wraps(f)
        def check_validity(*args, **kwargs):
            with statsd.Timer(__name__).time("check_validity"):
                errors = {"missing": [], "invalid": []}
                for error in validator.iter_errors(instance=kwargs):
                    if error.validator == "required":
                        error_pointer = JsonPointer.from_parts(
                            [*error.absolute_path, error.validator_value[0]]
                        )
                        errors["missing"].append(error_pointer.path)
                    else:
                        error_pointer = JsonPointer.from_parts(
                            error.absolute_path
                        )

                        errors["invalid"].append(
                            {
                                "context": error.validator,
                                "message": error.message,
                                "cause": str(error.cause)
                                if error.cause
                                else None,
                                "property": error_pointer.path,
                            }
                        )

                if len(errors["missing"]) or len(errors["invalid"]):
                    raise ValidationError(errors)

            return f(*args, **kwargs)

        return check_validity

    return validity_wrapper
