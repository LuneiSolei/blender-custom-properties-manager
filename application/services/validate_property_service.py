import bpy
from ...core import utils

class ValidatePropertyService:
    """Service for validating property data"""

    def validate_property(self, data_path: str, property_name: str, operator) -> bool:
        """
        Validate a property's existence from a data path.
        :param data_path: Path to the Blender object.
        :param property_name: Name of the property to validate.
        :param operator: Operator from which the property is evaluated.
        """

        data_object = utils.resolve_data_object(bpy.context, data_path)
        if not data_object:
            operator.report({'ERROR'}, f"Data object for '{data_path}' not found")

            return False

        if property_name not in data_object:
            operator.report({'ERROR'}, f"Property '{property_name}' not found in {data_object.name}")

            return False

        return True

