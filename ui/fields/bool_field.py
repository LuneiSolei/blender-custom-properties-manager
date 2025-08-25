from .field import Field

class BoolField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_value(self, value):
        pass

