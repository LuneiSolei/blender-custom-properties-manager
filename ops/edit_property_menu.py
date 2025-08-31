import bpy

from .edit_property_menu_mixin import EditPropertyMenuOperatorMixin
from .. import consts
from ..core import GroupData, utils
from ..ui.fields.field_factory import FieldFactory

class EditPropertyMenuOperator(bpy.types.Operator, EditPropertyMenuOperatorMixin):

    def invoke(self, context, event):
        if not self._validate():
            return {'CANCELLED'}

        if not self._load_ui_data():
            return {'CANCELLED'}

        self._get_property_data()
        self._setup_fields()

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        self._group_data = GroupData.get_data(self.data_object)
        self._group_data.set_operator(self)

        # NOTE: self.property_overridable_library_set('["prop"]',
        #  True/False) is how you change the "is_overridable_library" attribute
        # Apply modified properties
        for name, field in self._fields.items():
            field.apply(self)

        # Redraw Custom Properties panel
        for area in context.screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()

        return {'FINISHED'}

    def draw(self, context):
        for name, field in self._fields.items():
            # Determine if the field should be drawn
            if not field.should_draw(self.type):
                continue

            field_row = field.draw(self)

            # Enable/Disable the soft min/max fields
            if (field.ui_data_attr == "soft_max" or
                    field.ui_data_attr == "soft_min"):
                field_row.enabled = self.use_soft_limits

    def _validate(self) -> bool:
        """Validate input data and prepare object references"""
        self.data_object = utils.resolve_data_object(bpy.context, self.data_path)
        if not self.data_object:
            self.report({'ERROR'}, "Data object '{}' not found".format(self.data_path))

            return False

        self.data_object_name = self.data_object.name

        if self.name not in self.data_object:
            self.report({'ERROR'}, "Property '{}' not found".format(self.name))

            return False

        return True

    def _load_ui_data(self):
        """Load existing property UI data"""
        self.ui_data = (self.data_object
                        .id_properties_ui(self.name)
                        .as_dict())

        return True

    def _get_property_data(self):
        self.value = self.data_object[self.name]

        # noinspection PyTypeChecker
        self.type = utils.get_property_type_from_value(self.value)

    def _setup_fields(self):
        """Helper method to set up data for fields"""

        # Populate self._fields with pre-defined configs
        for field_name in consts.fields.fieldConfigs:
            field_config = consts.fields.fieldConfigs[field_name]
            new_field = FieldFactory().create(
                **vars(field_config),
                property_type = self.type
            )
            new_field.current_value = self._find_value(new_field.attr_name)
            self._fields[field_name] = new_field

    def _find_value(self, attr_name: str):
        if attr_name in self.ui_data:
            return self.ui_data[attr_name]
        elif attr_name == consts.fields.FieldNames.GROUP:
            # noinspection PyTypeChecker
            self.group = GroupData.get_data(self.data_object).get_group_name(self.name)
            return self.group

        return getattr(self, attr_name)

    def _is_use_soft_limits(self) -> bool:
        limit_attrs = {}
        for field in self._processed_fields:
            if field.ui_data_attr in ["min", "soft_min", "max", "soft_max"]:
                limit_attrs[field.ui_data_attr] = getattr(self, field.attr_name)

        return (limit_attrs.get("min") != limit_attrs.get("soft_min") or
                limit_attrs.get("max") != limit_attrs.get("soft_max"))

    # TODO: Move to field products
    def _apply_name(self):
        # Make sure the property name has changed
        current_name = self._current["name"]
        new_name = self.name
        if current_name == new_name:
            return

        # Validation
        if new_name in self.data_object:
            self.report({'ERROR'}, f"Property '{new_name}' already exists")
            return

        # Ensure we're not trying to rename an IDPropertyGroup
        if isinstance(self.data_object[current_name], bpy.types.bpy_struct):
            self.report({'ERROR'}, f"Cannot rename '{current_name}' to '"
                                   f"{new_name}'. Renaming IDPropertyGroup "
                                   f"types is currently not supported.")

            return

        # Update the property in CPM's dataset
        self._group_data.update_property_name(
            data_object=self.data_object,
            prop_name=current_name,
            new_name=new_name
        )

        # Update the property in the data object itself
        self.data_object[new_name] = self.data_object[current_name]
        self.data_object.id_properties_ui(new_name).update(**self.ui_data)
        del self.data_object[current_name]

    def _apply_group(self):
        # Make sure the group name has changed
        old_group = self._current["group"]
        new_group = self.group
        if old_group == new_group:
            return

        # Update property in CPM's dataset
        group_data = GroupData.get_data(self.data_object)
        group_data.set_operator(self)
        group_data.update_property_group(
            data_object=self.data_object,
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