import bpy

class UIDataService:
    def load(self, data_object: bpy.types.Object, property_name: str) -> dict:
        """
        Loads the UI data for the provided Blender data object.
        :param data_object: Blender data object.
        :param property_name: Name of the property.
        :return: A dictionary representing the UI data.
        """

        return data_object.id_properties_ui(property_name).as_dict()