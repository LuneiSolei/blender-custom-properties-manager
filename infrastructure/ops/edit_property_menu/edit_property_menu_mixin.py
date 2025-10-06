from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty, CollectionProperty
from ....application.services import PropertyTypeService, field_validation_service
from ....shared import consts
from .default_array_element import DefaultArrayElement

# noinspection PyTypeHints
class EditPropertyMenuOperatorMixin:
    bl_label = "Edit Property"
    bl_idname = consts.CPM_EDIT_PROPERTY
    bl_description = "Edit custom property menu"

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
    array_length: IntProperty(
        min = consts.ARRAY_LENGTH_MIN,
        max = consts.ARRAY_LENGTH_MAX,
        update = field_validation_service.on_array_length_update
    )
    default_array: CollectionProperty(type = DefaultArrayElement)

    # FLOAT
    default_float: FloatProperty()
    min_float: FloatProperty(update = field_validation_service.on_min_max_float_update)
    max_float: FloatProperty(update = field_validation_service.on_min_max_float_update)
    soft_min_float: FloatProperty(update = field_validation_service.on_soft_min_max_float_update)
    soft_max_float: FloatProperty(update = field_validation_service.on_soft_min_max_float_update)
    subtype_float: EnumProperty(items = consts.PROPERTY_SUBTYPES)
    subtype_array_float: EnumProperty(items = consts.PROPERTY_SUBTYPE_VECTORS)

    # INT
    default_int: IntProperty()
    min_int: IntProperty(update = field_validation_service.on_min_max_int_update)
    max_int: IntProperty(update = field_validation_service.on_min_max_int_update)
    soft_min_int: IntProperty(update = field_validation_service.on_soft_min_max_int_update)
    soft_max_int: IntProperty(update = field_validation_service.on_soft_min_max_int_update)
    subtype_int: EnumProperty(items = consts.PROPERTY_SUBTYPES)
    subtype_array_int: EnumProperty(items = consts.PROPERTY_SUBTYPE_VECTORS)

    # Misc.
    _group_data = {}
    _current = {}
    fields: StringProperty() = "{}"