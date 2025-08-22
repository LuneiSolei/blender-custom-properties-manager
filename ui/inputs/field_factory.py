from typing import Optional
from .field import Field
from .int_field import IntField
from .text_field import TextField
from .float_field import FloatField
from .bool_field import BoolField
from .arrays.float_array_field import FloatArrayField
from .arrays.int_array_field import IntArrayField
from .arrays.bool_array_field import BoolArrayField

class FieldFactory:

    @staticmethod
    def create_field(field_type: str) -> Optional[Field]:
        match field_type:
            case 'FLOAT':
                return FloatField()
            case 'INT':
                return IntField()
            case 'BOOL':
                return BoolField()
            case 'STRING':
                return TextField()
            case 'FLOAT_ARRAY':
                return FloatArrayField()
            case 'INT_ARRAY':
                return IntArrayField()
            case 'BOOL_ARRAY':
                return BoolArrayField()
            case 'PYTHON':
                return TextField()
            case _:
                raise NotImplementedError

        return None