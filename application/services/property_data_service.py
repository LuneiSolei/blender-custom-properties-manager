import bpy
from ...core import utils

# noinspection PyMethodMayBeStatic
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

    def get_ui_data(self, data_object: bpy.types.Object, property_name: str):
        """
        Loads the UI data for the provided Blender data object.

        Example UI data for various types
            FLOAT: {
                'subtype': 'NONE',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.0,
                'soft_max': 1.0,
                'step': 0.10000000149011612,
                'precision': 3,
                'default': 1.0
            }

            FLOAT_ARRAY: {
                'subtype': 'NONE',
                'description': '',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.29999998211860657,
                'soft_max': 1.0,
                'step': 0.10000000149011612,
                'precision': 3,
                'default': [0.3700000047683716, 0.3700000047683716, 0.3700000047683716]
            }
        :param data_object: Blender data object.
        :param property_name: Name of the property.
        :return: An object used to manage the UI data.
        """

        return data_object.id_properties_ui(property_name)

    def validate(self, data_path: str, property_name: str, operator) -> bpy.types.Object:
        """
        Validate a property's existence from a data path.
        :param data_path: Path to the Blender object.
        :param property_name: Name of the property to validate.
        :param operator: Operator from which the property is evaluated.
        :return: True if the property is valid, False otherwise.
        """

        data_object = utils.resolve_data_object(bpy.context, data_path)
        if not data_object:
            operator.report({'ERROR'}, f"Data object for '{data_path}' not found")

            return None

        if property_name not in data_object:
            operator.report({'ERROR'}, f"Property '{property_name}' not found in {data_object.name}")

            return None

        return data_object