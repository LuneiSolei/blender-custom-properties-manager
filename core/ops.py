import bpy
from bpy.props import (StringProperty, EnumProperty, BoolProperty,
                       FloatProperty, IntProperty, FloatVectorProperty,
                       IntVectorProperty, BoolVectorProperty)
from .group_data import GroupData
from .state import cpm_state
from . import utilities as utils
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
    # If removed, PyCharm will complain about the PyTypes.
    # Property attributes
    data_path:              utils.blender_prop(str, StringProperty)
    property_name:          utils.blender_prop(str, StringProperty)
    property_type:          utils.blender_prop(str, EnumProperty,
                                items = config.CUSTOM_PROPERTY_TYPE_ITEMS)
    group_name:             utils.blender_prop(str, StringProperty)
    use_soft_limits:        utils.blender_prop(bool, BoolProperty)
    array_length:           utils.blender_prop(int, IntProperty)
    precision_float:        utils.blender_prop(int, IntProperty)
    precision_float_array:  utils.blender_prop(int, IntProperty)
    subtype_float:          utils.blender_prop(str, EnumProperty,
                                items = config.PROPERTY_SUBTYPE_ITEMS)
    subtype_float_array:    utils.blender_prop(str, EnumProperty,
                                items = config.PROPERTY_SUBTYPE_VECTOR_ITEMS)
    description:            utils.blender_prop(str, StringProperty)
    is_overridable_library: utils.blender_prop(bool, BoolProperty)

    # Min values
    min_float:              utils.blender_prop(float, FloatProperty)
    min_float_array:        utils.blender_prop(float, FloatProperty)
    min_int:                utils.blender_prop(int, IntProperty)
    min_int_array:          utils.blender_prop(int, IntProperty)
    soft_min_float:         utils.blender_prop(float, FloatProperty)
    soft_min_float_array:   utils.blender_prop(float, FloatProperty)
    soft_min_int:           utils.blender_prop(int, IntProperty)
    soft_min_int_array:     utils.blender_prop(int, IntProperty)

    # Max values
    max_float:              utils.blender_prop(float, FloatProperty)
    max_float_array:        utils.blender_prop(float, FloatProperty)
    max_int:                utils.blender_prop(int, IntProperty)
    max_int_array:          utils.blender_prop(int, IntProperty)
    soft_max_float:         utils.blender_prop(float, FloatProperty)
    soft_max_float_array:   utils.blender_prop(float, FloatProperty)
    soft_max_int:           utils.blender_prop(int, IntProperty)
    soft_max_int_array:     utils.blender_prop(int, IntProperty)

    # Step values
    step_float:             utils.blender_prop(float, FloatProperty)
    step_float_array:       utils.blender_prop(float, FloatProperty)
    step_int:               utils.blender_prop(int, IntProperty)
    step_int_array:         utils.blender_prop(int, IntProperty)

    # Default values
    default_float:          utils.blender_prop(float, FloatProperty)
    default_float_array:    utils.blender_prop(list[float], FloatVectorProperty)
    default_int:            utils.blender_prop(int, IntProperty)
    default_int_array:      utils.blender_prop(list[int], IntVectorProperty)
    default_bool:           utils.blender_prop(bool, BoolProperty)
    default_bool_array:     utils.blender_prop(bool, BoolVectorProperty)
    default_string:         utils.blender_prop(str, StringProperty)
    default_data_block:     utils.blender_prop(str, StringProperty)
    default_python:         utils.blender_prop(str, StringProperty)

    # True values
    value_float:            utils.blender_prop(float, FloatProperty)
    value_float_array:      utils.blender_prop(list[float], FloatVectorProperty)
    value_int:              utils.blender_prop(int, IntProperty)
    value_int_array:        utils.blender_prop(list[int], IntVectorProperty)
    value_bool:             utils.blender_prop(bool, BoolProperty)
    value_bool_array:       utils.blender_prop(bool, BoolVectorProperty)
    value_string:           utils.blender_prop(str, StringProperty)
    value_data_block:       utils.blender_prop(str, StringProperty)
    value_python:           utils.blender_prop(str, StringProperty)

    def invoke(self, context, event):
        # Initialize the edit property menu
        if not self._validate():
            return {'CANCELLED'}

        if not self._load_prop_ui_data():
            return {'CANCELLED'}

        self._setup_fields()

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # NOTE: self.property_overridable_library_set('["prop"]',
        #  True/False) is how you change the "is_overridable_library" attribute
        # Apply modified properties
        self._apply_name()
        self._apply_group()

        # Redraw Custom Properties panel
        for area in context.screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()

        return {'FINISHED'}

    def _validate(self) -> bool:
        """Validate input data and prepare object references"""
        self._data_object = utils.resolve_data_object(bpy.context, self.data_path)
        if not self._data_object:
            self.report({'ERROR'}, "Data object '{}' not found".format(self.data_path))
            return False

        self.data_object_name = self._data_object.name
        self._current = {
            "name": self.property_name,
            "group": self.group_name,
            "type": self.property_type,
        }

        if self.property_name not in self._data_object:
            self.report({'ERROR'}, "Property '{}' not found".format(self.property_name))
            return False

        return True

    def _load_prop_ui_data(self):
        """Load existing property UI data"""
        self._ui_data = (self._data_object
                         .id_properties_ui(self.property_name)
                         .as_dict())

        return True

    def _setup_fields(self):
        """Setup field values form existing property data"""
        self.property_type = self._get_property_type()
        self._processed_fields = []
        deferred_fields = []

        for field in config.fields:
            # Create a copy of the field to avoid modifying the original
            processed_field = self._process_field(field)
            if field.attr_name == "use_soft_limits":
                deferred_fields.append(processed_field)
            else:
                self._processed_fields.append(processed_field)

        # Process deferred fields
        for field in deferred_fields:
            self.use_soft_limits = self._is_use_soft_limits()
            self._processed_fields.append(field)

    def _process_field(self, field: config.Field) -> config.Field:
        """Process individual field and set its value"""
        attr_name = field.attr_name
        if field.attr_name == "property_type":
            attr_name = field.attr_name
        elif field.attr_name == "is_overridable_library":
            override_str = f'["{self.property_name}"]'
            self.is_overridable_library = (
                self._data_object.is_property_overridable_library(override_str))
            attr_name = field.attr_name
        elif field.attr_name == "description":
            value = self._ui_data.get(field.ui_data_attr, "")
            setattr(self, attr_name, value)
        elif field.attr_prefix == "value_":
            attr_name = f"{field.attr_prefix}{self.property_type.lower()}"
            value = self._data_object[self.property_name]
            setattr(self, attr_name, value)
        elif field.attr_prefix:
            attr_name = f"{field.attr_prefix}{self.property_type.lower()}"
            value = self._ui_data.get(field.ui_data_attr)
            if value is not None:
                setattr(self, attr_name, value)

        return config.Field(
            label = field.label,
            attr_prefix = field.attr_prefix,
            ui_data_attr = field.ui_data_attr,
            attr_name = attr_name,
            draw_on = field.draw_on)

    def draw(self, context):
        for field in self._processed_fields:
            if not self._should_draw_field(field):
                continue

            # Enable/Disable the soft min/max fields
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
        limit_attrs = {}
        for field in self._processed_fields:
            if field.ui_data_attr in ["min", "soft_min", "max", "soft_max"]:
                limit_attrs[field.ui_data_attr] = getattr(self, field.attr_name)

        return (limit_attrs.get("min") != limit_attrs.get("soft_min") or
                limit_attrs.get("max") != limit_attrs.get("soft_max"))

    def _should_draw_field(self, field: config.Field) -> bool:
        """Determine if the field should be drawn based on property type"""
        return self.property_type in field.draw_on or field.draw_on == "ALL"

    def _apply_name(self):
        # Make sure the property name has changed
        old_name = self._current["name"]
        new_name = self.property_name
        if old_name == new_name:
            return

        # Does the new name already exist?
        if new_name in self._data_object:
            self.report({'ERROR'}, f"Property '{new_name}' already exists")
            return

        # Ensure we're not trying to rename an IDPropertyGroup
        if type(self._data_object[old_name]).__name__ == "IDPropertyGroup":
            self.report({'ERROR'}, f"Cannot rename '{old_name}' to '"
                                   f"{new_name}'. Renaming IDPropertyGroup "
                                   f"types is currently not supported.")
            return

        # Update the property in CPM's dataset
        group_data = GroupData.get_data(self._data_object)
        group_data.set_operator(self)
        group_data.update_property_name(
            data_object = self._data_object,
            prop_name = old_name,
            new_name = new_name)

        # Update the property in the data object itself
        self._data_object[new_name] = self._data_object[old_name]
        self._data_object.id_properties_ui(new_name).update(**self._ui_data)
        del self._data_object[old_name]

    def _apply_group(self):
        # Make sure the group name has changed
        old_group = self._current["group"]
        new_group = self.group_name
        if old_group == new_group:
            return

        # Update property in CPM's dataset
        group_data = GroupData.get_data(self._data_object)
        group_data.set_operator(self)
        group_data.update_property_group(
            data_object = self._data_object,
            prop_name = self.property_name,
            new_group = new_group)

    def _apply_type(self):
        # Make sure the property type has changed
        old_type = self._current["type"]
        new_type = self.property_type
        if old_type == new_type:
            return

        # Update the property in the data object
        self._ui_data["type"] = new_type
        self._data_object.id_properties_ui(self.property_name).update(**self._ui_data)