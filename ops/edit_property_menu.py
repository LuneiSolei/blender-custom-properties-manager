# Blender imports
import bpy

# CPM imports
from .edit_property_menu_mixin import EditPropertyMenuOperatorMixin
from ..core import GroupData, utils
from ..ui.fields.field import Field
from ..ui.fields.field_factory import FieldFactory

class EditPropertyMenuOperator(bpy.types.Operator, EditPropertyMenuOperatorMixin):

    def invoke(self, context, event):
        # Initialize the edit property menu
        if not self._validate():
            return {'CANCELLED'}

        if not self._load_prop_ui_data():
            return {'CANCELLED'}

        self._get_property_data()
        self._setup_fields()

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # NOTE: self.property_overridable_library_set('["prop"]',
        #  True/False) is how you change the "is_overridable_library" attribute
        # Apply modified properties
        self._apply_name()
        self._apply_group()
        self._apply_type()

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

        if self.name not in self._data_object:
            self.report({'ERROR'}, "Property '{}' not found".format(self.name))
            return False

        return True

    def _load_prop_ui_data(self):
        """Load existing property UI data"""
        self._ui_data = (self._data_object
                         .id_properties_ui(self.name)
                         .as_dict())

        return True

    def _get_property_data(self):
        self.value = self._data_object[self.name]
        self.type = utils.get_property_type_from_value(self.value)

    def _setup_fields(self):
        """Setup field values from existing property data"""

        # Determine which fields need to be populated and drawn
        string_field = FieldFactory().create_field(
            field_type='STRING',
            name="name",
            label="Property Name",
            draw_on="ALL",
            attr_prefix=None,
            ui_data_attr=None,
            attr_name="name"
        )

        self._processed_fields = []
        deferred_fields = []

        self._processed_fields.append(string_field)

        # fields = Field.create_fields()
        # self._processed_fields = []
        # deferred_fields = []
        #
        # for field in fields:
        #     # Create a copy of the field to avoid modifying the original
        #     processed_field = self._process_field(field)
        #     if field.attr_name == "use_soft_limits":
        #         deferred_fields.append(processed_field)
        #     else:
        #         self._processed_fields.append(processed_field)
        #
        # # Process deferred fields
        # for field in deferred_fields:
        #     self.use_soft_limits = self._is_use_soft_limits()
        #     self._processed_fields.append(field)

    def _process_field(self, field: Field) -> Field:
        """Process individual field and set its value"""

        # attr_name = field.attr_name
        # match field.id:
        #     case "name":
        #         self._current["name"] = self.name
        #     case "description":
        #         self._current["description"] = self.description
        #     case "group":
        #         self._current["group"] = self.group_name
        #     case "type":
        #         value = self._data_object[self.name]
        #         self._current["type"] = self.type
        #
        # return

        # if field.id == "type":
        #     value = self._data_object[self.name]
        #     self.type = utils.get_property_type_from_value(value)
        # elif field.id == "overridable_library":
        #     override_str = f'["{self.name}"]'
        #     self.is_overridable_library = (
        #         self._data_object.is_property_overridable_library(override_str))
        # elif field.id == "description":
        #     value = self._ui_data.get(field.ui_data_attr, "")
        #     setattr(self, attr_name, value)
        # elif field.id == "value":
        #     attr_name = f"{field.attr_prefix}{self.type.lower()}"
        #     value = self._data_object[self.name]
        #     setattr(self, attr_name, value)
        #     self._current["value"] = value
        # elif field.attr_prefix:
        #     attr_name = f"{field.attr_prefix}{self.type.lower()}"
        #     value = self._ui_data.get(field.ui_data_attr)
        #     if value is not None:
        #         setattr(self, attr_name, value)
        #
        # return Field(
        #     id = field.id,
        #     label = field.label,
        #     attr_prefix = field.attr_prefix,
        #     ui_data_attr = field.ui_data_attr,
        #     attr_name = attr_name,
        #     draw_on = field.draw_on)

    def draw(self, context):
        for field in self._processed_fields:
            if not self._should_draw_field(field):
                continue

            # Enable/Disable the soft min/max fields
            prop_row = self._draw_aligned_prop(field)
            if (field.ui_data_attr == "soft_max" or
                    field.ui_data_attr == "soft_min"):
                prop_row.enabled = self.use_soft_limits

    def _draw_aligned_prop(self, field: Field) -> bpy.types.UILayout:
        row = self.layout.row()
        split = row.split(factor=0.5)

        # Create left column
        left_col = split.column()
        left_col.alignment = 'RIGHT'
        left_col.label(text=field.label)

        # Create right column
        right_col = split.column()
        right_col.prop(data=self, property=field.attr_name, text="")

        return row

    def _is_use_soft_limits(self) -> bool:
        limit_attrs = {}
        for field in self._processed_fields:
            if field.ui_data_attr in ["min", "soft_min", "max", "soft_max"]:
                limit_attrs[field.ui_data_attr] = getattr(self, field.attr_name)

        return (limit_attrs.get("min") != limit_attrs.get("soft_min") or
                limit_attrs.get("max") != limit_attrs.get("soft_max"))

    def _should_draw_field(self, field: Field) -> bool:
        """Determine if the field should be drawn based on property type"""
        return self.type in field.draw_on or field.draw_on == "ALL"

    def _apply_name(self):
        # Make sure the property name has changed
        old_name = self._current["name"]
        new_name = self.name
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
            data_object=self._data_object,
            prop_name=old_name,
            new_name=new_name)

        # Update the property in the data object itself
        self._data_object[new_name] = self._data_object[old_name]
        self._data_object.id_properties_ui(new_name).update(**self._ui_data)
        del self._data_object[old_name]

    def _apply_group(self):
        # Make sure the group name has changed
        old_group = self._current["group"]
        new_group = self.group
        if old_group == new_group:
            return

        # Update property in CPM's dataset
        group_data = GroupData.get_data(self._data_object)
        group_data.set_operator(self)
        group_data.update_property_group(
            data_object=self._data_object,
            prop_name=self.name,
            new_group=new_group)

    def _apply_type(self):
        # Make sure the property type has changed
        old_type = self._current["type"]
        new_type = self.type
        if old_type == new_type:
            return

        # Update the property in the data object
        if self.type == 'FLOAT':
            return bpy.props.FloatProperty(
                name=self.name,
                description=self.description,
                translation_context="",
                min=self.min,
                max=self.max,
                soft_min=self.soft_min,
                soft_max=self.soft_max,
                step=self.step,
                precision=self.precision,
                options=self.options,
                override=self.override,
                tags=self.tags,
                subtype=self.subtype,
                unit=self.unit,
                update=self.update,
                get=self.get,
                set=self.set
            )

    def _apply_value(self):
        # Make sure the property value has changed
        old_value = self._current["value"]