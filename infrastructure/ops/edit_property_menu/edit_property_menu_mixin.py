import bpy

from typing import Union
from bpy.props import (BoolProperty, BoolVectorProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty,
                       IntVectorProperty, StringProperty)
from ....shared import consts
from ....application.managers import PropertyDataManager

# noinspection PyTypeHints
class EditPropertyMenuOperatorMixin:
    bl_label = "Edit Property"
    bl_idname = consts.CPM_EDIT_PROPERTY
    bl_description = "Edit custom property menu"

    # Needed for PyCharm to properly property_type check against Blender's EnumProperty.
    # If removed, PyCharm will complain about the PyTypes.
    # Property attributes
    data_path: StringProperty()
    data_object: StringProperty()
    ui_data: StringProperty()
    name: StringProperty()
    property_type: EnumProperty(
        items = consts.PROPERTY_TYPES,
        update = PropertyDataManager.on_type_change
    )
    group: StringProperty()
    value_float: FloatProperty()
    value_int: IntProperty()
    value_bool: BoolProperty()
    value_string: StringProperty()
    step: IntProperty()
    precision: IntProperty()
    subtype_float: EnumProperty(items = consts.PROPERTY_SUBTYPES)
    initialized: BoolProperty(default = False)

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
    subtype_float: EnumProperty(items = consts.PROPERTY_SUBTYPES)
    subtype_float_array: EnumProperty(items = consts.PROPERTY_SUBTYPE_VECTORS)
    description: StringProperty()
    is_overridable_library: BoolProperty()

    # Misc.
    _group_data = {}
    _current = {}
    fields: StringProperty() = "{}"