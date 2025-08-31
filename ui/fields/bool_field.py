from .field import Field

class BoolField(Field):
    _current_value: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, new_value):
        pass