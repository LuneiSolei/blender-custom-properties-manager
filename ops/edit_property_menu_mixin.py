from typing import Any, Union

from bpy.props import (BoolProperty, BoolVectorProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty,
                       IntVectorProperty, StringProperty)

from .. import consts

# noinspection PyTypeHints
class EditPropertyMenuOperatorMixin:
    bl_label = "Edit Property"
    bl_idname = consts.ops.CPM_EDIT_PROPERTY
    bl_description = "Edit custom property menu"

    # Needed for PyCharm to properly type check against Blender's EnumProperty.
    # If removed, PyCharm will complain about the PyTypes.
    # Property attributes
    data_path: StringProperty()
    name: StringProperty()
    type: EnumProperty(items=consts.blender_enums.CUSTOM_PROPERTY_TYPE_ITEMS)
    group: StringProperty()
    value: Any

    min: Union[FloatProperty(), FloatVectorProperty(), IntProperty(), IntVectorProperty()]
    max: Union[FloatProperty(), FloatVectorProperty(), IntProperty(), IntVectorProperty()]
    soft_min: Union[FloatProperty(), FloatVectorProperty(), IntProperty(), IntVectorProperty()]
    soft_max: Union[FloatProperty(), FloatVectorProperty(), IntProperty(), IntVectorProperty()]

    step: Union[FloatProperty(), FloatVectorProperty(), IntProperty(), IntVectorProperty()]
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
    precision_float: IntProperty()
    precision_float_array: IntProperty()
    subtype_float: EnumProperty(items=consts.blender_enums.PROPERTY_SUBTYPE_ITEMS)
    subtype_float_array: EnumProperty(items=consts.blender_enums.PROPERTY_SUBTYPE_VECTOR_ITEMS)
    description: StringProperty()
    is_overridable_library: BoolProperty()

    # Misc.
    _group_data = {}
    _current = {}
    _fields = {}