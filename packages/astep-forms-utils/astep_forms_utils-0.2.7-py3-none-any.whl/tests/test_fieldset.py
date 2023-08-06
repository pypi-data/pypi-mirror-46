from astep_form_utils import FieldSet, StringField


class FakeRequest:
    def __init__(self, values):
        self.values = values
        self.files = {}


def test_validate_positive():
    field_set = FieldSet(
        StringField("test")
    )
    assert field_set.is_valid(FakeRequest({"test": "foo"}))


def test_validate_negative():
    field_set = FieldSet(
        StringField("test")
    )

    assert not field_set.is_valid(FakeRequest({"test": 1}))
