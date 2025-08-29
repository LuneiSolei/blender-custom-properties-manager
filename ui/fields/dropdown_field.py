from enum import Enum

from .field import Field

class DropdownField(Field):
    _current_value: Enum

    def __init__(self, **kwargs):
        super().__init__(**kwargs)