import bpy
from bpy.props import (StringProperty, EnumProperty, BoolProperty,
                       FloatProperty, IntProperty, FloatVectorProperty,
                       IntVectorProperty, BoolVectorProperty)
from typing import TYPE_CHECKING
from .state import cpm_state
from . import config, utilities

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
    data_path: str if TYPE_CHECKING else StringProperty()
    property_name: str if TYPE_CHECKING else StringProperty()
    is_overridable_library: bool if TYPE_CHECKING else BoolProperty()
    description: str if TYPE_CHECKING else StringProperty()
    use_soft_limits: bool if TYPE_CHECKING else BoolProperty()
    property_type: str if TYPE_CHECKING else EnumProperty(
        items = config.RNA_CUSTOM_PROPERTY_TYPE_ITEMS
    )
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
        # Get the target property
        self._data_object = (utilities.resolve_data_object(context, self.data_path))

        if not self.property_name in self._data_object:
            # The property does not exist in the data_object
            self.report({'ERROR'}, "Property '{}' not found".format(self.property_name))
            return {'CANCELLED'}

        # Determine the property's type from Blender's provided enums
        self._set_property_type(self._data_object)

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):
        # context.active_object[]

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        # Create type row
        self._draw_aligned_row(label = config.PROP_TYPE_LABEL,
                               prop_name = config.PROP_TYPE_PROP)

        # Create default value row
        prop_name = "default_" + self.property_type.lower()
        self._draw_aligned_row(label = config.DEFAULT_VALUE_LABEL,
                               prop_name= prop_name)


    def _set_property_type(self, data_object: bpy.types.Object):
        """
        Gets the string property type of the property of the provided object.
            :param data_object: The Blender object the property is in.
        """

        # Determine property type
        target_prop = data_object[self.property_name]
        prop_type = type(target_prop).__name__
        match prop_type:
            case "float":
                self.property_type = 'FLOAT'
            case "int":
                self.property_type = 'INT'
            case "bool":
                self.property_type = 'BOOL'
            case "string":
                self.property_type = 'STRING'
            case "IDPropertyArray":
                # Property is an array type
                if len(target_prop) > 0:
                    if isinstance(target_prop[0], float):
                        self.property_type = 'FLOAT_ARRAY'
                    elif isinstance(target_prop[0], int):
                        self.property_type = 'INT_ARRAY'
                    elif isinstance(target_prop[0], bool):
                        self.property_type = 'BOOL_ARRAY'
                    else:
                        self.property_type = 'FLOAT_ARRAY'
                else:
                    self.property_type = 'FLOAT_ARRAY'
            case "IDPropertyGroup":
                self.property_type = 'PYTHON'
            case _ if isinstance(target_prop, bpy.types.ID):
                self.property_type = 'DATA_BLOCK'
            case _:
                self.property_type = 'FLOAT'

    def _draw_aligned_row(self, label: str, prop_name: str):
        row = self.layout.row()
        split = row.split(factor = 0.5)

        # Create left column
        left_col = split.column()
        left_col.alignment = config.ALIGN_RIGHT
        left_col.label(text = label)

        # Create right column
        right_col = split.column()
        right_col.prop(data = self, property = prop_name, text ="")