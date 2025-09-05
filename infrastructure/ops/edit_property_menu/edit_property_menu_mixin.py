import bpy

from typing import Any, Union
from bpy.props import (BoolProperty, BoolVectorProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty,
                       IntVectorProperty, StringProperty)
from ....shared import ops, blender_enums

# noinspection PyTypeHints
class EditPropertyMenuOperatorMixin:
    bl_label = "Edit Property"
    bl_idname = ops.CPM_EDIT_PROPERTY
    bl_description = "Edit custom property menu"

    # Services Cache
    property_data_service: Any
    edit_property_service: Any
    field_service: Any

    # Needed for PyCharm to properly type check against Blender's EnumProperty.
    # If removed, PyCharm will complain about the PyTypes.
    # Property attributes
    data_path: StringProperty()
    data_object: bpy.types.Object
    ui_data: dict
    name: StringProperty()
    type: EnumProperty(items = blender_enums.CUSTOM_PROPERTY_TYPE_ITEMS)
    group: StringProperty()
    value_float: FloatProperty()
    value_int: IntProperty()
    value_bool: BoolProperty()
    value_string: StringProperty()
    step: IntProperty()
    precision: IntProperty()
    subtype_float: EnumProperty(items = blender_enums.PROPERTY_SUBTYPE_ITEMS)

    # FLOAT
    min_float: FloatProperty()
    max_float: FloatProperty()
    soft_min_float: FloatProperty()
    soft_max_float: FloatProperty()

    # INT
    min_int: IntProperty()
    max_int: IntProperty()
    soft_min_int: IntProperty()
    soft_max_int: IntProperty()

    default: Union[
        FloatProperty(),
        FloatVectorProperty(),
        IntProperty(),
        IntVectorProperty(),
        BoolProperty(),
        BoolVectorProperty(),
        StringProperty()
    ]
    use_soft_limits: BoolProperty()
    array_length: IntProperty()
    subtype_float: EnumProperty(items = blender_enums.PROPERTY_SUBTYPE_ITEMS)
    subtype_float_array: EnumProperty(items = blender_enums.PROPERTY_SUBTYPE_VECTOR_ITEMS)
    description: StringProperty()
    is_overridable_library: BoolProperty()

    # Misc.
    _group_data = {}
    _current = {}
    fields = {}