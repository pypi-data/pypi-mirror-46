"""
Module to simplify the development of API services for the aSTEP service,
and to DRY the required code.

Exposes FieldSet, which is used to both verify the values sent from the API as well as to generate
the list of fields shown in the input form on the UI.

Also exposes individual fields, which should be used to define what is expected, of each input type.
These can be easily extended to add more types, as requirements grow.

"""
from typing import Callable, Tuple

from .exceptions import *
from .types import *


def is_data_empty(data: Dict[str, Any]) -> bool:
    """
    As the UI sends every field, but with empty values, we need to verify whether
    it actually sends any data
    :param data: data from request
    :return: whether the request is basically empty
    """
    return not any([bool(value) for key, value in data.items()])


class FieldSet:
    """
    Collection of fields
    """

    def __init__(self, fields: List[Field]):
        self.fields = fields
        self.cleaned_data: Dict[str, Any] = {}
        self.errors = []

    def is_valid(self, data: Dict[str, Any]) -> bool:
        """
        Validate all input. should be run before
        handling input. cleaned data will be empty until this is run.
        Every exception thrown by the fields, will be written to the self.error buffer
        These can be shown to the user
        :param data: A JSON dict
        :return: whether the output was relevant.
        """
        # clear values in case the instance, even though prohibited, are reused.
        self.errors = []
        self.cleaned_data = {}

        # unpack fields with subfields
        def validate_fields(
                unvalidated_fields
        ) -> Tuple[Dict[str, Any], List[ValidationError]]:
            cleaned_data: Dict[str, Any] = {}
            errors: List[ValidationError] = []
            for field in unvalidated_fields:
                try:
                    value = field.validate(data.get(field.name))
                    cleaned_data[field.name] = value
                    if issubclass(type(field), SubfieldsPromise):
                        sub_field_output = validate_fields(field.get_subfields(value))
                        cleaned_data = {**cleaned_data, **sub_field_output[0]}
                        errors += sub_field_output[1]

                except ValidationError as error:
                    errors.append(error)
            return cleaned_data, errors

        self.cleaned_data, self.errors = validate_fields(self.fields)

        return len(self.errors) == 0

    def render_errors(self):
        """
        Renders all ValidationErrors caught to an error list
        :return:
        """
        error_texts = [str(error) for error in self.errors]
        html_list = f"<ul><li>{'</li><li>'.join(error_texts)}</li></ul>"
        return {
            "chart_type": "text",
            "content": (
                "<div style='color: red'>"
                f"Some input supplied was invalid!<br>{html_list}"
                "</div>"
            ),
        }

    def as_form_fields(self):
        """
        Renders all fields to JSON type expected by UI
        :return: response for form-area
        """
        return [field.as_form_field() for field in self.fields]


def field_set_factory(*fields: Field) -> Callable[[], FieldSet]:
    """
    Factory for creating a fieldset.
    :param fields: the fields to base the fieldset on
    :return: a function that creates a unique fieldset
    """
    return lambda: FieldSet(list(fields))
