from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email

from schematizer.exceptions import CompoundValidationError, SimpleValidationError
from schematizer.validators import BaseValidator


def _convert_validation_error(validation_error):
    errors = []
    for error in validation_error.error_list:
        extra = dict(error.params) if error.params else {}
        extra.update(message=error.message % extra)
        errors.append(
            SimpleValidationError(error.code.upper(), extra=extra),
        )
    return CompoundValidationError(errors)


class URL(BaseValidator):
    def validate_native(self, obj):
        validate_url = URLValidator()
        try:
            validate_url(obj)
        except ValidationError as error:
            raise _convert_validation_error(error) from error


class Email(BaseValidator):
    def validate_native(self, obj):
        try:
            validate_email(obj)
        except ValidationError as error:
            raise _convert_validation_error(error) from error


class Password(BaseValidator):
    def validate_native(self, obj):
        try:
            validate_password(obj)
        except ValidationError as error:
            raise _convert_validation_error(error) from error
