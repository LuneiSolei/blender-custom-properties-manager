from typing import Union

from bpy.props import (BoolProperty, BoolVectorProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty,
                       IntVectorProperty, StringProperty)
from ....application.services import PropertyTypeService, field_validation_service
from ....shared import consts

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
        update = PropertyTypeService.on_type_change
    )
    group: StringProperty()
    description: StringProperty()
    step_float: FloatProperty()
    step_int: IntProperty()
    precision: IntProperty()
    initialized: BoolProperty(default = False)
    use_soft_limits: BoolProperty()
    is_property_overridable_library: BoolProperty()
    array_length: IntProperty()

    # FLOAT
    default_float: FloatProperty()
    default_float_array: FloatVectorProperty()
    min_float: FloatProperty(update = field_validation_service.on_min_max_float_update)
    max_float: FloatProperty(update = field_validation_service.on_min_max_float_update)
    soft_min_float: FloatProperty(update = field_validation_service.on_soft_min_max_float_update)
    soft_max_float: FloatProperty(update = field_validation_service.on_soft_min_max_float_update)
    subtype_float: EnumProperty(items = consts.PROPERTY_SUBTYPES)
    subtype_array_float: EnumProperty(items = consts.PROPERTY_SUBTYPE_VECTORS)

    # INT
    default_int: IntProperty()
    default_int_array: IntVectorProperty()
    min_int: IntProperty(update = field_validation_service.on_min_max_int_update)
    max_int: IntProperty(update = field_validation_service.on_min_max_int_update)
    soft_min_int: IntProperty(update = field_validation_service.on_soft_min_max_int_update)
    soft_max_int: IntProperty(update = field_validation_service.on_soft_min_max_int_update)
    subtype_int: EnumProperty(items = consts.PROPERTY_SUBTYPES)
    subtype_array_int: EnumProperty(items = consts.PROPERTY_SUBTYPE_VECTORS)

    default: Union[
        FloatProperty(),
        FloatVectorProperty(),
        IntProperty(),
        IntVectorProperty(),
        BoolProperty(),
        BoolVectorProperty(),
        StringProperty()
    ]
    array_length: IntProperty()

    # Misc.
    _group_data = {}
    _current = {}
    fields: StringProperty() = "{}"