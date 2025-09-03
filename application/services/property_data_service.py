import bpy

class PropertyDataService:
    def get_type(self, data_object: bpy.types.Object, property_name: str) -> str:
        """
        Get property type from data object.
        :param data_object: Blender data object
        :param property_name: Name of the property
        :return: One of the following:
            'FLOAT',
            'FLOAT_ARRAY',
            'INT',
            'INT_ARRAY',
            'BOOL',
            'BOOL_ARRAY',
            'STRING',
            'PYTHON',
            'DATA_BLOCK'
        """
        types = {
            "float": 'FLOAT',
            "float_array": 'FLOAT_ARRAY',
            "int": 'INT',
            "int_array": 'INT_ARRAY',
            "bool": 'BOOL',
            "bool_array": 'BOOL_ARRAY',
            "string": 'STRING',
            "IDPropertyGroup": 'PYTHON',
            "data_block": 'DATA_BLOCK'
        }
        value = data_object[property_name]
        prop_type = type(value).__name__
        if prop_type in types:
            # Property is of a standard type
            return types[prop_type]
        elif prop_type == "IDPropertyArray":
            # Property is of an array type
            has_values = len(value) > 0

            if has_values and isinstance(value[0], float):
                return types["float_array"]
            elif has_values and isinstance(value[0], int):
                return types["int_array"]
            elif has_values and isinstance(value[0], bool):
                return types["bool_array"]
            else:
                return types["float_array"]
        elif isinstance(value, bpy.types.ID):
            # Property is of a data_block type
            return types["data_block"]
        else:
            # Property type could not be determined. Theoretically, this should never happen
            return types["float"]

    def get_ui_data(self, data_object: bpy.types.Object, property_name: str) -> dict:
        """
        Loads the UI data for the provided Blender data object.
        :param data_object: Blender data object.
        :param property_name: Name of the property.
        :return: A dictionary representing the UI data.
        """

        return data_object.id_properties_ui(property_name).as_dict()