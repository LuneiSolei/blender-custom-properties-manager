from .field import Field

class IntField(Field):
    _current_value: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)