from operator import indexOf

import bpy
from bpy.props import (StringProperty, EnumProperty, BoolProperty,
                       FloatProperty, IntProperty, FloatVectorProperty,
                       IntVectorProperty, BoolVectorProperty)
from typing import TYPE_CHECKING, Any
from collections import namedtuple
from .state import cpm_state
from . import utilities
from .. import config

class AddNewPropertyGroupOperator(bpy.types.Operator):
    bl_label = "New Group"
    bl_idname = config.CPM_ADD_NEW_PROPERTY_GROUP_OP
    bl_description = "Add a new custom property group"
    bl_options = {'REGISTER', 'UNDO'}

    data_path: StringProperty(
        name = "Data Path",
        description = "Path to the target object",
        default = "Object"
    )

    def execute(self, context):
        target = getattr(bpy.types, self.data_path)
        target["my_property"] = 1.0
        self.report({'INFO'}, "Added new custom property group")

        return {'FINISHED'}

class ExpandToggleOperator(bpy.types.Operator):
    """Toggle expand/collapse state for property groups"""
    bl_idname = config.CPM_EXPAND_TOGGLE_OP
    bl_label = "Toggle Expand"
    bl_description = "Toggle the expand/collapse state of a property group"

    expand_key: bpy.props.StringProperty(
        name = "Expand Key",
        description = "Unique key for this expand state"
    )
    current_state: bpy.props.BoolProperty(
        name = "Current State",
        description = "Current expand/collapse state"
    )

    def execute(self, context):
        cpm_state.expand_states[self.expand_key] = not self.current_state

        return {'FINISHED'}

# noinspection PyAttributeOutsideInit
class EditPropertyPopupOperator(bpy.types.Operator):
    bl_label = "Edit Property"
    bl_idname = config.CPM_EDIT_PROPERTY_OP
    bl_description = "Edit custom property menu"

    # Needed for PyCharm to properly type check against Blender's EnumProperty.
    # If removed, PyCharm will complain that property_type expects None.
    # Property attributes
    property_type: str if TYPE_CHECKING \
        else EnumProperty(items = config.CUSTOM_PROPERTY_TYPE_ITEMS)
    data_path: str if TYPE_CHECKING else StringProperty()
    property_name: str if TYPE_CHECKING else StringProperty()
    group_name: str if TYPE_CHECKING else StringProperty()
    use_soft_limits: bool if TYPE_CHECKING else BoolProperty()
    array_length: int if TYPE_CHECKING else IntProperty()
    precision_float: int if TYPE_CHECKING else IntProperty()
    precision_float_array: list[int] if TYPE_CHECKING else IntVectorProperty()
    subtype_normal: str if TYPE_CHECKING \
        else EnumProperty(items = config.PROPERTY_SUBTYPE_ITEMS)
    subtype_array: str if TYPE_CHECKING \
        else EnumProperty(items = config.PROPERTY_SUBTYPE_VECTOR_ITEMS)
    description: str if TYPE_CHECKING else StringProperty()
    is_overridable_library: bool if TYPE_CHECKING else BoolProperty()

    # Min values
    min_float: float if TYPE_CHECKING else FloatProperty()
    min_float_array: list[float] if TYPE_CHECKING else FloatVectorProperty()
    min_int: int if TYPE_CHECKING else IntProperty()
    min_int_array: list[int] if TYPE_CHECKING else IntVectorProperty()
    soft_min_float: float if TYPE_CHECKING else FloatProperty()
    soft_min_float_array: list[float] if TYPE_CHECKING else FloatVectorProperty()
    soft_min_int: int if TYPE_CHECKING else IntProperty()
    soft_min_int_array: list[int] if TYPE_CHECKING else IntVectorProperty()

    # Max values
    max_float: float if TYPE_CHECKING else FloatProperty()
    max_float_array: list[float] if TYPE_CHECKING else FloatVectorProperty()
    max_int: int if TYPE_CHECKING else IntProperty()
    max_int_array: list[int] if TYPE_CHECKING else IntVectorProperty()
    soft_max_float: float if TYPE_CHECKING else FloatProperty()
    soft_max_float_array: list[float] if TYPE_CHECKING else FloatVectorProperty()
    soft_max_int: int if TYPE_CHECKING else IntProperty()
    soft_max_int_array: list[int] if TYPE_CHECKING else IntVectorProperty()

    # Step values
    step_float: float if TYPE_CHECKING else FloatProperty()
    step_float_array: list[float] if TYPE_CHECKING else FloatVectorProperty()
    step_int: int if TYPE_CHECKING else IntProperty()
    step_int_array: list[int] if TYPE_CHECKING else IntVectorProperty()

    # Default values
    default_float: float if TYPE_CHECKING else FloatProperty()
    default_float_array: list[float] if TYPE_CHECKING else FloatVectorProperty()
    default_int: int if TYPE_CHECKING else IntProperty()
    default_int_array: list[int] if TYPE_CHECKING else IntVectorProperty()
    default_bool: bool if TYPE_CHECKING else BoolProperty()
    default_bool_array: list[bool] if TYPE_CHECKING else BoolVectorProperty()
    default_string: str if TYPE_CHECKING else StringProperty()
    default_data_block: str if TYPE_CHECKING else StringProperty()
    default_python: str if TYPE_CHECKING else StringProperty()

    def invoke(self, context, event):
        # Prepare the edit property menu
        # Get the target property
        self._data_object = (utilities.resolve_data_object(context, self.data_path))

        # Verify property exists in data object
        if not self.property_name in self._data_object:
            # The property does not exist in the data_object
            self.report({'ERROR'}, "Property '{}' not found".format(self.property_name))
            return {'CANCELLED'}

        # Retrieve Blender's already stored UI data for the property
        self._ui_data = (self._data_object
                         .id_properties_ui(self.property_name)
                         .as_dict())

        # Start setting the field values
        deferred = []
        for index, field in enumerate(config.fields):
            # Programmatically adjust field values. "property_name" does not need
            # any adjustments
            attr_name = field.attr_name
            if field.attr_name == "property_type":
                self.property_type = self._get_property_type()
            elif field.attr_name == "use_soft_limits":
                # Ensure that min/max values are retrieved first
                deferred.append((index, field))
            elif field.attr_name != "property_name":
                attr_name = field.attr_prefix + self.property_type.lower()
                value = self._ui_data.get(field.ui_data_attr)
                setattr(self, attr_name, value)

            config.fields[index] = config.Field(
                label = field.label,
                attr_prefix = field.attr_prefix,
                ui_data_attr = field.ui_data_attr,
                attr_name = attr_name,
                draw_on = field.draw_on)

        for index, field in deferred:
            # Perform "use_soft_limits" calculations
            self.use_soft_limits = self._is_use_soft_limits()

            config.fields[index] = config.Field(
                label = field.label,
                attr_prefix = field.attr_prefix,
                ui_data_attr = field.ui_data_attr,
                attr_name = field.attr_name,
                draw_on = field.draw_on)

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # context.active_object[]

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        for field in config.fields:
            if not self.property_type in field.draw_on and not field.draw_on == 'ALL':
                continue

            prop_row = self._draw_aligned_prop(field)
            if (field.ui_data_attr == "soft_max" or
                field.ui_data_attr == "soft_min"):
                prop_row.enabled = self.use_soft_limits

    def _draw_aligned_prop(self, field: config.Field) -> bpy.types.UILayout:
        row = self.layout.row()
        split = row.split(factor = 0.5)

        # Create left column
        left_col = split.column()
        left_col.alignment = config.ALIGN_RIGHT
        left_col.label(text = field.label)

        # Create right column
        right_col = split.column()
        right_col.prop(data = self, property = field.attr_name, text = "")

        return row

    def _get_property_type(self) -> str:
        """
        Gets the type of the property.
        :return: The property's type as determined by Blender.
        """

        # Determine property type
        target_prop = self._data_object[self.property_name]
        prop_type = type(target_prop).__name__
        match prop_type:
            case "float":
                return 'FLOAT'
            case "int":
                return 'INT'
            case "bool":
                return 'BOOL'
            case "str":
                return 'STRING'
            case "IDPropertyArray":
                # Property is an array type
                if len(target_prop) > 0:
                    if isinstance(target_prop[0], float):
                        return 'FLOAT_ARRAY'
                    elif isinstance(target_prop[0], int):
                        return 'INT_ARRAY'
                    elif isinstance(target_prop[0], bool):
                        return 'BOOL_ARRAY'
                    else:
                        return 'FLOAT_ARRAY'
                else:
                    return 'FLOAT_ARRAY'
            case "IDPropertyGroup":
                return 'PYTHON'
            case _ if isinstance(target_prop, bpy.types.ID):
                return 'DATA_BLOCK'
            case _:
                return 'FLOAT'

    def _is_use_soft_limits(self) -> bool:
        attr_names = {
            "min": None,
            "soft_min": None,
            "max": None,
            "soft_max": None}

        # Get hard and soft min/max values
        for field in config.fields:
            if field.ui_data_attr in attr_names:
                attr_names[field.ui_data_attr] = getattr(self, field.attr_name)

        return (attr_names["min"] != attr_names["soft_min"] or
                attr_names["max"] != attr_names["soft_max"])