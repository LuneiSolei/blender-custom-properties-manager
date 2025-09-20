import bpy

from .edit_property_menu_mixin import EditPropertyMenuOperatorMixin
from ....application.managers import GroupDataManager, PropertyDataManager, FieldManager

class EditPropertyMenuOperator(bpy.types.Operator, EditPropertyMenuOperatorMixin):
    _group_data_manager: type[GroupDataManager]
    _property_data_manager: type[PropertyDataManager]
    _field_manager: type[FieldManager]

    @classmethod
    def initialize(cls,
            group_data_manager: type[GroupDataManager],
            property_data_manager: type[PropertyDataManager],
            field_manager: type[FieldManager]):
        """Initialize the operator with its dependencies."""

        cls._group_data_manager = group_data_manager
        cls._property_data_manager = property_data_manager
        cls._field_manager = field_manager

    def invoke(self, context, _):
        self.data_object = self._property_data_manager.validate(
            data_path = self.data_path,
            property_name = self.name,
            operator = self
        )
        if not self.data_object:
            return {'CANCELLED'}

        self.ui_data = self._property_data_manager.get_ui_data(
            data_object = self.data_object,
            property_name = self.name
        ).as_dict()
        if not self.ui_data:
            return {'CANCELLED'}

        # noinspection PyAttributeOutsideInit
        self.value = self.data_object[self.name]

        # Flag to prevent type change callback during initial setup
        self.initialized = False

        # noinspection PyTypeChecker
        self.type = self._property_data_manager.get_type(
            data_object = self.data_object,
            property_name = self.name
        )

        self.fields = self._field_manager.setup_fields(self)
        self.initialized = True

        # Show the menu as a popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        self._group_data = self._group_data_manager.get_data(self.data_object)
        self._group_data.set_operator(self)

        # NOTE: self.property_overridable_library_set('["prop"]',
        # True/False) is how you change the "is_overridable_library" attribute
        # Apply modified properties
        self._property_data_manager.update_property_data(self)

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