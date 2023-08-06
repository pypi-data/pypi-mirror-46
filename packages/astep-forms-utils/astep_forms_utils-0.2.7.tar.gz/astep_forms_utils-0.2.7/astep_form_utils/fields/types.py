"""
Defines the different fields and their types.
This exposes the base class (which shouldn't be used directly) and different fields.
You can easily implement your own field, much like the implementation of the fields here.
It requires implementation of validate (see implementations for examples)
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, Any, Dict, Type, List, Optional

from werkzeug.datastructures import FileStorage

from .exceptions import ValidationError, NullValueValidationError


class Field(ABC):
    """
    Abstract base class for the field type.
    Shouldn't be initialized directly.
    """

    def __init__(self, name: str, label: Optional[str] = None,
                 default: Optional[Any] = None, help_text: Optional[str] = None):
        """
        Initialize base class for fields
        :param name: Name of the field (in code, cleaned_data)
        :param label: label as shown in UI
        """
        self.name = name
        self.label = label or name.replace("_", " ").title()
        self.help_text = help_text
        self.default = default

    def validate(self, value: Union[str, float]) -> Any:
        """
        Validate whether the value is allowed / expected.
        If the value is invalid, a ValidationError is thrown.
        Should set self.value!
        :param value: the raw value from the UI
        :return: the value of the field
        """
        raise NotImplementedError

    @abstractmethod
    def as_form_field(self) -> Dict[str, Any]:
        """
        Generate the field into the JSON dict expected by the UI to render list of fields.
        Any implementation should explode the returned dict into the array returned.
        :return:
        """
        return {"name": self.name, "label": self.label, "default":self.default}


class SubfieldsPromise(ABC):
    """
    Inherit from this if your field has subfields.
    This will make the fieldset look at the subfields returned from the {get_subfields} function
    """

    def get_subfields(self, parent_value: Any) -> List[Field]:
        """
        Get subfields of this field. This is manually implemented in implementations.
        :param parent_value: value of parent field,
        if that value is relevant. this depends on implementation
        :return: a list of sub fields
        """
        raise NotImplementedError


class FloatField(Field):
    """
    Field for storing a float value
    """

    def as_form_field(self) -> Dict[str, Any]:
        return {**super().as_form_field(), **{"type": "input-number"}}

    def validate(self, value: Union[str, float]) -> Any:
        if value.isnumeric():
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        raise ValidationError(self.name, f"Value '{value}' is not a float")


class StringField(Field):
    """
    Field for handling a text area / string.
    """

    def as_form_field(self) -> Dict[str, Any]:
        return {**super().as_form_field(), **{"type": "input"}}

    def validate(self, value: str) -> str:
        if isinstance(value, str):
            return value
        raise ValidationError(self.name, f"Value '{value}' is not a string")


class BoolField(Field):
    """
    Field for storing a string value
    """

    def as_form_field(self) -> Dict[str, Any]:
        return {
            **super().as_form_field(),
            **{
                "type": "checkbox",
                "default": "true" if self.default else "false"
            }
        }

    def validate(self, value: Union[str, bool]) -> Any:
        if isinstance(value, (bool, int)):
            return bool(value)
        if isinstance(value, str) and value.lower() in ["true", "false", ""]:
            return value.lower() == "true"
        raise ValidationError(self.name, f"Value '{value}' is not a bool")


class FileField(Field):
    """
    Field for handling file upload.
    """

    def __init__(self, name: str, label: Optional[str] = None,
                 help_text: Optional[str] = None):
        super().__init__(name=name, label=label, default=None, help_text=help_text)

    def as_form_field(self) -> Dict[str, Any]:
        return {**super().as_form_field(), **{"type": "file"}}

    def validate(self, value: FileStorage) -> FileStorage:
        if isinstance(value, FileStorage):
            return value

        raise ValidationError(self.name, f"Value '{value}' is not a File")


class EnumField(Field):
    """
    Field for an enum value.
    """

    def __init__(self, name: str, options: Type[Enum], label=None, default=None, help_text=None):
        """
        An enum single-pick field.
        :param name: Name of the field (in code, cleaned_data)
        :param options: the enum type
        :param label: label as shown in UI
        """
        super().__init__(name=name, label=label, help_text=help_text, default=default)
        self.options = options

    def validate(self, value: Union[str, float]):
        if not value.strip():
            raise NullValueValidationError(self.name)

        try:
            # HTML forms normally make everything into an string, so this reverts this ://
            if value.isnumeric():
                value = float(value)
            return [e for e in self.options if e.value == value][0]
        except IndexError:
            if list(*self.options):
                stringed_options = [f"'{o}'" for o in self.options]
                listing_options = (
                    f"{', '.join(stringed_options[:-1])} or {stringed_options[-1]}"
                )
            else:
                listing_options = f"{self.options[0]}"
            raise ValidationError(
                self.name,
                f"Value '{value}' not accepted. should be either {listing_options}",
            )

    def as_form_field(self):
        return {
            **super().as_form_field(),
            **{
                "type": "select",
                "options": [{"name": str(o), "value": o.value} for o in self.options],
            },
        }


class SubFieldsEnumField(EnumField, SubfieldsPromise):
    """
    Enum field with subfields attached.
    """

    def __init__(
            self,
            name: str,
            options: Type[Enum],
            sub_fields: Dict[Enum, List[Field]],
            label: Optional[str] = None,
            help_text: Optional[str] = None,
            default: Enum = None,
    ):
        """
        :param name: Name of the field (in code, cleaned_data)
        :param options: the enum type
        :param sub_fields: a dict of eac enum element to a list of fields (if given enum doesn't
        exist then an empty list is assumed)
        :param label: label as shown in UI
        """
        super().__init__(name, options, label=label, help_text=help_text, default=default)
        self.sub_fields = sub_fields

    def get_subfields(self, parent_value: Enum) -> List[Field]:
        return self.sub_fields[parent_value] if parent_value in self.sub_fields else []

    def as_form_field(self):
        def generate_option_data(option):
            if option in self.sub_fields:
                fields = [field.as_form_field() for field in self.sub_fields[option]]
            else:
                fields = []
            return {"name": str(option), "value": option.value, "fields": fields}

        return {
            **super().as_form_field(),
            **{
                "type": "formset-select",
                "options": [generate_option_data(option) for option in self.options],
            },
        }
