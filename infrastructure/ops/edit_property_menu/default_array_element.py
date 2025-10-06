import bpy
from bpy.props import FloatProperty, IntProperty, BoolProperty

# noinspection PyTypeHints
class DefaultArrayElement(bpy.types.PropertyGroup):
    float_value: FloatProperty()
    int_value: IntProperty()
    bool_value: BoolProperty()