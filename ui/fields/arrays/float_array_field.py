from .array_field import ArrayField

class FloatArrayField(ArrayField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)