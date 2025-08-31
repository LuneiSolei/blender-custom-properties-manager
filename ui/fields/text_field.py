import bpy

from ...core import ReportingMixin, GroupData
from .field import Field

class TextField(Field, ReportingMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, operator):
        # Format method name with "apply_" prefix
        method_name = f"apply_{self.attr_name}"

        # Call the method by name using the method's object
        method = getattr(self, method_name)
        method(operator)

    def apply_name(self, operator):
        new_name = operator.name
        current_name = self.current_value
        if new_name == current_name:
            return

        # Validate the new name
        data_object = operator.data_object
        if new_name in data_object:
            self.report({'ERROR'}, f"Property '{new_name}' already exists")
            operator.name = current_name

            return

        # Renaming IDPropertyGroups is not supported
        if isinstance(data_object[self.current_value], bpy.types.bpy_struct):
            self.report({'ERROR'}, f"Cannot rename '{self.current_value}' to '{new_name}'. "
                                   f"Renaming IDPropertyGroup types is currently not supported.")

            return

        # Update property name in CPM's dataset
        GroupData.get_data(data_object).update_property_name(
            data_object = data_object,
            prop_name = self.current_value,
            new_name = new_name
        )

        # Update the property name in the data object itself
        data_object[new_name] = data_object[self.current_value]
        data_object.id_properties_ui(new_name).update(**operator.ui_data)
        del data_object[self.current_value]

    def apply_group(self, operator):
        # Check that group name has changed
        current_group = self.current_value
        new_group = operator.group
        if new_group == current_group:
            return

        # Update property group in CPM's dataset
        GroupData.get_data(operator.data_object).update_property_group(
            data_object = operator.data_object,
            prop_name = operator.name,
            new_group = new_group
        )