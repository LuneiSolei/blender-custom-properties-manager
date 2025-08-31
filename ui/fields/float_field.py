import bpy
from .field import Field

class FloatField(Field):
    # noinspection PyTypeHints
    value: bpy.props.FloatProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 2.0

    def apply(self, new_value):
        pass