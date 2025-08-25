from .array_field import ArrayField

class BoolArrayField(ArrayField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)