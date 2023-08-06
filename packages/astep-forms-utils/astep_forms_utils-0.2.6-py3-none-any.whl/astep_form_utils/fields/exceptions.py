"""
All exceptions that can be returned from the UI
"""


class ValidationError(Exception):
    """
    Error with invalid data passed to a form field
    """

    def __init__(self, field_name, description):
        """
        Initialize a validation eror
        :param field_name: the name of the field that fails
        :param description: Description of the given error
        """
        super().__init__(f"{field_name}: {description}")


class NullValueValidationError(ValidationError):
    """
    A specific implementation of ValidationError for reused purpose
    """

    def __init__(self, field_name):
        """
        Initialize NullValueValidationError
        :param field_name: the name of the field that fails
        """
        super().__init__(field_name, "Dont accept a null value.")
