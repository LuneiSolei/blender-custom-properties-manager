from bpy.props import (StringProperty, EnumProperty, BoolProperty,
                       FloatProperty, IntProperty, FloatVectorProperty,
                       IntVectorProperty, BoolVectorProperty)
from typing import Any
from .. import config

# noinspection PyTypeHints
class EditPropertyMenuOperatorMixin:
    bl_label = "Edit Property"
    bl_idname = config.CPM_EDIT_PROPERTY_OP
    bl_description = "Edit custom property menu"

    # Needed for PyCharm to properly type check against Blender's EnumProperty.
    # If removed, PyCharm will complain about the PyTypes.
    # Property attributes
    data_path: StringProperty()
    name: StringProperty()
    type: EnumProperty(items=config.CUSTOM_PROPERTY_TYPE_ITEMS)
    group: StringProperty()
    value: Any
    use_soft_limits: BoolProperty()
    array_length: IntProperty()
    precision_float: IntProperty()
    precision_float_array: IntProperty()
    subtype_float: EnumProperty(items=config.PROPERTY_SUBTYPE_ITEMS)
    subtype_float_array: EnumProperty(items=config.PROPERTY_SUBTYPE_VECTOR_ITEMS)
    description: StringProperty()
    is_overridable_library: BoolProperty()

    # Min values
    min_float: FloatProperty()
    min_float_array: FloatProperty()
    min_int: IntProperty()
    min_int_array: IntProperty()
    soft_min_float: FloatProperty()
    soft_min_float_array: FloatProperty()
    soft_min_int: IntProperty()
    soft_min_int_array: IntProperty()

    # Max values
    max_float: FloatProperty()
    max_float_array: FloatProperty()
    max_int: IntProperty()
    max_int_array: IntProperty()
    soft_max_float: FloatProperty()
    soft_max_float_array: FloatProperty()
    soft_max_int: IntProperty()
    soft_max_int_array: IntProperty()

    # Step values
    step_float: FloatProperty()
    step_float_array: FloatProperty()
    step_int: IntProperty()
    step_int_array: IntProperty()

    # Default values
    default_float: FloatProperty()
    default_float_array: FloatVectorProperty()
    default_int: IntProperty()
    default_int_array: IntVectorProperty()
    default_bool: BoolProperty()
    default_bool_array: BoolVectorProperty()
    default_string: StringProperty()
    default_data_block: StringProperty()
    default_python: StringProperty()

    # True values
    value_float: FloatProperty()
    value_float_array: FloatVectorProperty()
    value_int: IntProperty()
    value_int_array: IntVectorProperty()
    value_bool: BoolProperty()
    value_bool_array: BoolVectorProperty()
    value_string: StringProperty()
    value_data_block: StringProperty()
    value_python: StringProperty()

    # Misc.
    _current = {}