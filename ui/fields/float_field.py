from .field import Field

class FloatField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)