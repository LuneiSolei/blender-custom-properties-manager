import bpy
from .apply_handler import ApplyHandler
from ...core import Field, GroupData

class ApplyNameHandler(ApplyHandler):
    def handle(self, field: Field, operator):
        new_name = operator.name
        current_name = field.current_value
        if new_name == current_name:
            return

        # Validate the new name
        data_object = operator.data_object
        if new_name in data_object:
            field.report({'ERROR'}, f"Property '{new_name}' already exists")
            operator.name = current_name

            return

        # Renaming IDPropertyGroups is not supported
        if isinstance(data_object[field.current_value], bpy.types.bpy_struct):
            field.report({'ERROR'}, f"Cannot rename '{field.current_value}' to '{new_name}'. "
                                   f"Renaming IDPropertyGroup types is currently not supported.")

            return

        # Update property name in CPM's dataset
        GroupData.get_data(data_object).update_property_name(
            data_object = data_object,
            prop_name = field.current_value,
            new_name = new_name
        )

        # Update the property name in the data object itself
        data_object[new_name] = data_object[field.current_value]
        data_object.id_properties_ui(new_name).update(**operator.ui_data)
        del data_object[field.current_value]