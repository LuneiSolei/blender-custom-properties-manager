from .field import Field

class FloatField(Field):
    _current_value: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)