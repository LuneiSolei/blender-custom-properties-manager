import bpy
from typing import Any
from .edit_property_menu_mixin import EditPropertyMenuOperatorMixin
from ....application.managers import GroupDataManager, PropertyDataManager, FieldManager
from ....shared import consts, utils

class EditPropertyMenuOperator(bpy.types.Operator, EditPropertyMenuOperatorMixin):
    @classmethod
    def initialize(cls,
            group_data_manager: type[GroupDataManager],
            property_data_manager: type[PropertyDataManager],
            field_manager: type[FieldManager]):
        """Initialize the operator_instance with its dependencies."""
        cls.group_data_manager = group_data_manager
        cls.property_data_manager = property_data_manager
        cls.field_manager = field_manager

    # noinspection PyTypeChecker, PyAttributeOutsideInit
    def invoke(self, context, _):
        # Initialize the operator_instance
        self.value: Any = None
        self.initialized = False
        is_valid = self.property_data_manager.validate(
            data_path = self.data_path,
            property_name = self.name,
            operator = self
        )

        # Ensure data_object exists
        if not is_valid:
            return {'CANCELLED'}

        # Load UI data
        ui_data = self.property_data_manager.load_ui_data(operator_instance = self)
        self.ui_data = self.property_data_manager.stringify_ui_data(ui_data = ui_data)

        if not self.ui_data:
            return {'CANCELLED'}

        # Load additional property data
        data_object = utils.resolve_data_object(self.data_path)
        self.value = data_object[self.name]
        self.property_type = self.property_data_manager.get_type(operator_instance = self)
        operator_type = utils.get_blender_operator_type(consts.CPM_EDIT_PROPERTY)
        self.fields = self.field_manager.setup_fields(
            operator_instance = self,
            operator_type = operator_type
        )
        self.initialized= True

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        data_object = utils.resolve_data_object(self.data_path)
        self._group_data = self.group_data_manager.get_group_data(data_object)
        self._group_data.set_operator(self)

        # NOTE: self.property_overridable_library_set('["prop"]',
        # True/False) is how you change the "is_overridable_library" attribute
        # Apply modified properties
        self.property_data_manager.update_property_data(self)

        # Redraw the Custom Properties panel
        for area in context.screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()

        return {'FINISHED'}

    def draw(self, _):
        fields = self.field_manager.load_fields(self.fields)
        for name, field in fields.items():
            # Determine if the field should be drawn
            if not field.should_draw(self.property_type):
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