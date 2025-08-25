from .array_field import ArrayField

class IntArrayField(ArrayField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)