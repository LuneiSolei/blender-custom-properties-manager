from typing import Union

import bpy

from ...core import Field
from ...shared import consts, utils
from ...shared.entities import LogLevel
from ...shared.utils import StructuredLogger

class PropertyTypeService:
    logger = StructuredLogger(consts.MODULE_NAME)

    @classmethod
    def get_type(cls, operator_instance) -> str:
        """
        Get the property's type from the operator instance.

        :param operator_instance: The EditPropertyMenuOperator instance.

        :return: One of the PropertyTypes enum values
        """
        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Getting property type",
            extra = {
                "data_path": operator_instance.data_path,
                "prop_name": operator_instance.name,
            }
        )

        # Initialize property data
        data_object = utils.resolve_data_object(operator_instance.data_path)
        prop_name = operator_instance.name
        value = data_object[prop_name]
        prop_type = type(value).__name__
        return_value: str

        # Define a map to pair types with their Blender type equivalent
        type_map = {
            "float": consts.PropertyTypes.FLOAT,
            "float_array": consts.PropertyTypes.FLOAT_ARRAY,
            "int": consts.PropertyTypes.INT,
            "int_array": consts.PropertyTypes.INT_ARRAY,
            "bool": consts.PropertyTypes.BOOL,
            "bool_array": consts.PropertyTypes.BOOL_ARRAY,
            "string": consts.PropertyTypes.STRING,
            "IDPropertyGroup": consts.PropertyTypes.PYTHON,
            "data_block": consts.PropertyTypes.DATA_BLOCK
        }

        # Check if it's a standard property_type
        if prop_type in type_map:
            return_value = type_map[prop_type]

        # Check if it's an array property_type
        elif prop_type == consts.PropertyTypes.ID_PROPERTY_ARRAY:
            return_value = cls.determine_array_type(value)

        # Check if it's a data block property_type
        elif isinstance(value, bpy.types.ID):
            return_value = consts.PropertyTypes.DATA_BLOCK

        # Default fallback
        else:
            cls.logger.log(
                level = LogLevel.ERROR,
                message = "Property type not supported",
                extra = {
                    "property_type": prop_type
                }
            )

            return consts.PropertyTypes.FLOAT

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property type found",
            extra = {
                "property_type": prop_type,
            }
        )

        return return_value

    # noinspection PyUnboundLocalVariable
    @classmethod
    def determine_array_type(cls, value: list) -> consts.PropertyTypes:
        """
        Helper to determine the array property_type.

        :param value: The value of the array.

        :return: One of the PropertyTypes enum values.
        """
        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Determining array property type",
            extra = {
                "value": value
            }
        )

        return_value: consts.PropertyTypes
        if not value:
            # A value was not provided
            cls.logger.log(
                level = LogLevel.WARNING,
                message = "No value provided to determine array property type"
            )
            return consts.PropertyTypes.FLOAT_ARRAY

        match value[0]:
            case float():
                return_value = consts.PropertyTypes.FLOAT_ARRAY
            case int():
                return_value = consts.PropertyTypes.INT_ARRAY
            case bool():
                return_value = consts.PropertyTypes.BOOL_ARRAY
            case _:
                # We have an incorrect property type
                cls.logger.log(
                    level = LogLevel.ERROR,
                    message = "Array property type must be of float, int, or bool",
                    extra = {
                        "value": value[0],
                        "type": type(value[0])
                    }
                )
                return_value = consts.PropertyTypes.FLOAT_ARRAY

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Array property type found",
            extra = {
                "type": return_value
            }
        )

        return return_value

    @classmethod
    def update_type(cls, operator_instance, field: Field) -> str:
        """
        Helper to update the property's property_type.

        :param operator_instance: The EditMenuPropertyOperator instance.
        :param field: The field with the data used to update the property.

        :return: The updated property type.
        """
        old_type = cls.get_type(operator_instance)
        new_type = operator_instance.property_type
        old_value = operator_instance.value
        new_value: Union[int, float, bool, str, dict, list[int | float | bool]]

        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Updating property's type",
            extra = {
                "old_type": old_type,
                "new_type": new_type
            }
        )

        # Define a map convert Blender property types
        simple_type_converters = {
            consts.PropertyTypes.FLOAT: lambda v: float(v) if isinstance(v, (int, float)) else 0.0,
            consts.PropertyTypes.INT: lambda v: int(v) if isinstance(v, (int, float)) else 0,
            consts.PropertyTypes.BOOL: lambda v: bool(v),
            consts.PropertyTypes.STRING: lambda v: str(v),
            consts.PropertyTypes.PYTHON: lambda v: v if isinstance(v, dict) else {}
        }

        if new_type == old_type:
            # No need to change type
            return old_type

        if new_type in simple_type_converters:
            new_value = simple_type_converters[new_type](old_value)
        elif new_type in (consts.PropertyTypes.FLOAT_ARRAY,
                          consts.PropertyTypes.INT_ARRAY,
                          consts.PropertyTypes.BOOL_ARRAY):
            simple_type = new_type.removesuffix("_ARRAY")
            converter = simple_type_converters[simple_type]
            if isinstance(old_value, list):
                new_value = [converter(v) for v in old_value]
            else:
                new_value = [converter(old_value)]
        else:
            cls.logger.log(
                level = LogLevel.CRITICAL,
                message = "Could not determine new value",
                extra = {
                    "old_value": old_value,
                    "old_type": old_type,
                    "new_type": new_type
                }
            )

            return old_type

        # Update the property with the new value as the new property_type
        data_object = utils.resolve_data_object(operator_instance.data_path)
        data_object[operator_instance.name] = new_value

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Finished updating property's type",
            extra = {
                "old_value": old_value,
                "old_type": old_type,
                "new_value": new_value,
                "new_type": new_type
            }
        )

        return new_type

    @staticmethod
    def on_type_change(operator_instance, context):
        """
        Called when the property property_type changes.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param context: The Blender context.
        """

        # Prevent infinite recursion
        if not getattr(operator_instance, "initialized", False):
            return

        operator_type = utils.get_blender_operator_type(consts.CPM_EDIT_PROPERTY)
        operator_instance.fields = operator_type.field_manager.setup_fields(
            operator_instance = operator_instance,
            operator_type = operator_type,
            is_redraw = True
        )