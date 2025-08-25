from abc import ABC

from ..field import Field

class ArrayField(Field, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)