from pydantic import ValidationError


class CustomValidationError(ValidationError):
    def __str__(self):
        return "Validation Error: " + super().__str__()
