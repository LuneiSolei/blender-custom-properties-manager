from enum import EnumType

from .field import Field

class DropdownField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)