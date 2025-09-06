import bpy

from .edit_property_menu_mixin import EditPropertyMenuOperatorMixin
from ....application.managers import GroupDataManager, PropertyDataManager

class EditPropertyMenuOperator(bpy.types.Operator, EditPropertyMenuOperatorMixin):
    _group_data_manager: type[GroupDataManager]
    _property_data_manager: type[PropertyDataManager]

    @classmethod
    def initialize(cls, group_data_manager: type[GroupDataManager], property_data_manager: type[PropertyDataManager]):
        """Initialize the operator with its dependencies."""
        cls._group_data_manager = group_data_manager
        cls._property_data_manager = property_data_manager

    def invoke(self, context, _):
        self.data_object = self.property_data_service.validate(
            data_path = self.data_path,
            property_name = self.name,
            operator = self
        )
        if not self.data_object:
            return {'CANCELLED'}

        self.ui_data = self.property_data_service.get_ui_data(
            data_object = self.data_object,
            property_name = self.name
        ).as_dict()
        if not self.ui_data:
            return {'CANCELLED'}

        self.value = self.data_object[self.name]
        self.type = self.property_data_service.get_type(
            data_object = self.data_object,
            property_name = self.name
        )

        self.fields = self.field_service.setup_fields(self)

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        self._group_data = self._group_data_manager.get_data(self.data_object)
        self._group_data.set_operator(self)

        # NOTE: self.property_overridable_library_set('["prop"]',
        # True/False) is how you change the "is_overridable_library" attribute
        # Apply modified properties
        self.edit_property_service.update_property_data(self)

        # Redraw the Custom Properties panel
        for area in context.screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()

        return {'FINISHED'}

    def draw(self, _):
        for name, field in self.fields.items():
            # Determine if the field should be drawn
            if not field.should_draw(self.type):
                continue

            field_row = field.draw(self)

            # Enable/Disable the soft min/max fields
            if (field.ui_data_attr == "soft_max" or
                    field.ui_data_attr == "soft_min"):
                field_row.enabled = self.use_soft_limits

    def _is_use_soft_limits(self) -> bool:
        limit_attrs = {}
        for field in self._processed_fields:
            if field.ui_data_attr in ["min", "soft_min", "max", "soft_max"]:
                limit_attrs[field.ui_data_attr] = getattr(self, field.attr_name)

        return (limit_attrs.get("min") != limit_attrs.get("soft_min") or
                limit_attrs.get("max") != limit_attrs.get("soft_max"))

    # def _apply_name(self):
    #     # Make sure the property name has changed
    #     current_name = self._current["name"]
    #     new_name = self.name
    #     if current_name == new_name:
    #         return
    #
    #     # Validation
    #     if new_name in self.data_object:
    #         self.report({'ERROR'}, f"Property '{new_name}' already exists")
    #         return
    #
    #     # Ensure we're not trying to rename an IDPropertyGroup
    #     if isinstance(self.data_object[current_name], bpy.types.bpy_struct):
    #         self.report({'ERROR'}, f"Cannot rename '{current_name}' to '"
    #                                f"{new_name}'. Renaming IDPropertyGroup "
    #                                f"types is currently not supported.")
    #
    #         return
    #
    #     # Update the property in CPM's dataset
    #     self._group_data.update_property_name(
    #         data_object=self.data_object,
    #         key=current_name,
    #         new_name=new_name
    #     )
    #
    #     # Update the property in the data object itself
    #     self.data_object[new_name] = self.data_object[current_name]
    #     self.data_object.id_properties_ui(new_name).update(**self.ui_data)
    #     del self.data_object[current_name]
    #
    # def _apply_group(self):
    #     # Make sure the group name has changed
    #     old_group = self._current["group"]
    #     new_group = self.group
    #     if old_group == new_group:
    #         return
    #
    #     # Update property in CPM's dataset
    #     group_data = GroupData.get_data(self.data_object)
    #     group_data.set_operator(self)
    #     group_data.update_property_group(
    #         data_object=self.data_object,
    #         key=self.name,
    #         new_group=new_group)
    #
    # def _apply_type(self):
    #     # Make sure the property type has changed
    #     old_type = self._current["type"]
    #     new_type = self.type
    #     if old_type == new_type:
    #         return
    #
    #     # Update the property in the data object
    #     if self.type == 'FLOAT':
    #         return bpy.props.FloatProperty(
    #             name=self.name,
    #             description=self.description,
    #             translation_context="",
    #             min=self.min,
    #             max=self.max,
    #             soft_min=self.soft_min,
    #             soft_max=self.soft_max,
    #             step=self.step,
    #             precision=self.precision,
    #             options=self.options,
    #             override=self.override,
    #             tags=self.tags,
    #             subtype=self.subtype,
    #             unit=self.unit,
    #             update=self.update,
    #             get=self.get,
    #             set=self.set
    #         )
    #
    # def _apply_value(self):
    #     # Make sure the property value has changed
    #     old_value = self._current["value"]