import bpy

from ...core import ReportingMixin, GroupData
from .field import Field

class TextField(Field, ReportingMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, data_object: bpy.types.Object, new_value: str):
        if self.current_value == new_value:
            return

        # Format method name with "apply_" prefix
        method_name = f"apply_{self.attr_name}"

        # Call the method by name using the method's object
        method = getattr(self, method_name)
        method(data_object, new_value)

    def apply_name(self, data_object: bpy.types.Object, new_name: str):
        # Validate the new name
        if new_name in data_object:
            self.report({'ERROR'}, f"Property '{new_name}' already exists")

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
        ui_data = data_object.id_properties_ui(self.current_value).as_dict()
        data_object.id_properties_ui(new_name).update(**ui_data)
        del data_object[self.current_value]

        print("We should be here!")