from typing import Optional

from .arrays.bool_array_field import BoolArrayField
from .arrays.float_array_field import FloatArrayField
from .arrays.int_array_field import IntArrayField
from .bool_field import BoolField
from .field import Field
from .float_field import FloatField
from .int_field import IntField
from .text_field import TextField

class FieldFactory:
    _field_types = {
        'FLOAT': FloatField,
        'INT': IntField,
        'BOOL': BoolField,
        'STRING': TextField,
        'FLOAT_ARRAY': FloatArrayField,
        'INT_ARRAY': IntArrayField,
        'BOOL_ARRAY': BoolArrayField,
        'PYTHON': TextField
    }

    @staticmethod
    def create_field(field_type: str, **kwargs) -> Optional[Field]:
        if field_type not in FieldFactory._field_types:
            raise NotImplementedError(f"Field type {field_type} is not currently supported")

        field_class = FieldFactory._field_types[field_type]
        return field_class(**kwargs)