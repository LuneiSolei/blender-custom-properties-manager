from .field import Field

class FloatField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_value(self, value):
        pass

