from typing import Optional

from .arrays.bool_array_field import BoolArrayField
from .arrays.float_array_field import FloatArrayField
from .arrays.int_array_field import IntArrayField
from .bool_field import BoolField
from .dropdown_field import DropdownField
from .field import Field
from .float_field import FloatField
from .int_field import IntField
from .text_field import TextField

class FieldFactory:
    _field_types = {
        'FLOAT': FloatField,
        'INT': IntField,
        'BOOL': BoolField,
        'TEXT': TextField,
        'FLOAT_ARRAY': FloatArrayField,
        'INT_ARRAY': IntArrayField,
        'BOOL_ARRAY': BoolArrayField,
        'DROPDOWN': DropdownField
    }

    @staticmethod
    def create(field_type: str, **kwargs) -> Field:
        if field_type not in FieldFactory._field_types:
            raise NotImplementedError(f"Field type {field_type} is not currently supported")

        field_class = FieldFactory._field_types[field_type](**kwargs)
        return field_class