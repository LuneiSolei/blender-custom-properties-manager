import json

from typing import Any, Union
from ...core import Field, FieldNames, field_configs
from ...shared import consts, utils
from ...shared.utils import StructuredLogger
from ...shared.entities import LogLevel

class FieldManager:
    logger = StructuredLogger(consts.MODULE_NAME)

    @classmethod
    def setup_fields(cls, operator_instance, operator_type, is_redraw: bool = False) -> str:
        """
        Sets up the relevant fields for an EditPropertyMenu operator_instance instance.

        :param operator_instance: The EditPropertyMenu operator_instance instance.
        :param operator_type: The EditPropertyMenu type.
        :param is_redraw: Whether to redraw the fields after creation.

        :return: A string representing a list of fields.
        """
        fields = {}
        property_type = operator_instance.property_type

        # Populate fields with pre-defined configs
        for name, config in field_configs.items():
            new_field = Field(
                **vars(config),
                property_type = property_type
            )

            if new_field.should_draw(property_type):
                if new_field.attr_name == "default_array":
                    # Don't serialize the collection itself, just skip it.
                    # The collection is managed by on_array_length_update.
                    new_field.current_value = None
                elif is_redraw and new_field.draw_on != 'ALL':
                    # Use default values for type-specific fields during redraw
                    new_field.current_value = getattr(operator_instance, new_field.attr_name)
                else:
                    new_field.current_value = cls.find_value(
                        operator_instance = operator_instance,
                        operator_type = operator_type,
                        attr_name = new_field.attr_name,
                        ui_data_attr = new_field.ui_data_attr
                    )

                # Skip setattr for collection properties since they are read-only
                if new_field.attr_name != "default_array":
                    old_value = getattr(operator_instance, new_field.attr_name)
                    if old_value != new_field.current_value:
                        setattr(operator_instance, new_field.attr_name, new_field.current_value)

            fields[name] = new_field

        return cls.stringify_fields(fields)

    @classmethod
    def set_default_array_field(cls, operator_instance):
        prop_types = [
            consts.PropertyTypes.FLOAT_ARRAY,
            consts.PropertyTypes.INT_ARRAY,
            consts.PropertyTypes.BOOL_ARRAY
        ]

        value_map = {
            consts.PropertyTypes.FLOAT_ARRAY: "float_value",
            consts.PropertyTypes.INT_ARRAY: "int_value",
            consts.PropertyTypes.BOOL_ARRAY: "bool_value"
        }

        if operator_instance.property_type in prop_types:
            ui_data = json.loads(operator_instance.ui_data)
            default_values = cls._get_ui_data_value("default_array", ui_data, "default")

            # Clear and repopulate the collection
            operator_instance.default_array.clear()
            attr_name = value_map[operator_instance.property_type]
            for value in default_values:
                element = operator_instance.default_array.add()
                setattr(element, attr_name, value)

    @classmethod
    def stringify_fields(cls, fields: dict[str, Field]) -> str:
        """
        Convert a dictionary of fields to a JSON string.

        :param fields: A dictionary of fields to convert.

        :return: A JSON string representing the fields.
        """
        field_data = [field.as_dict() for field in fields.values()]

        return json.dumps(field_data)

    @classmethod
    def load_fields(cls, fields: str) -> dict[str, Field]:
        """
        Load fields from a JSON string.

        :param fields: A JSON string representing the fields.

        :return: A dictionary of fields.
        """
        field_list = json.loads(fields)
        return_value = {
            field_data["name"]: Field.from_dict(field_data)
            for field_data in field_list
        }

        return return_value

    @classmethod
    def find_value(cls, operator_instance, operator_type, attr_name: str, ui_data_attr: Union[str, None]) -> Any:
        """
        Find the value in the operator_instance based on the attr_name.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param operator_type: The Blender type of the operator_instance.
        :param attr_name: The name of the attribute to find the value of.
        :param ui_data_attr: The name of the attribute to find the UI data for.

        :return: The value of the attribute.
        """
        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Finding value for attribute name",
            extra = {
                "attr_name": attr_name,
                "ui_data_attr": ui_data_attr
            }
        )

        # Load the UI data
        ui_data = json.loads(operator_instance.ui_data)
        if ui_data is None:
            ui_data = operator_type.property_data_manager.load_ui_data(operator_instance)
            operator_instance.ui_data = ui_data

        jump_table = {
            "group": lambda: cls._get_group_value(operator_instance, operator_type),
            "is_property_overridable_library": lambda: cls._get_overridable_library_value(operator_instance),
            "default_python": lambda: cls._get_python_value(operator_instance)
        }

        is_ui_data = ui_data_attr is not None
        if is_ui_data:
            # Prioritize the `ui_data_attr` value from the field
            found_value = cls._get_ui_data_value(attr_name, ui_data, ui_data_attr)
        elif attr_name in jump_table:
            # Use attr_name as a secondary source if the field does not utilize `ui_data_attr`
            # Firstly, check for special cases
            found_value = jump_table[attr_name]()
        else:
            # Otherwise, use the value of the attribute tied to the operator instance
            found_value = getattr(operator_instance, attr_name)

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Found value for attribute",
            extra = {
                "attr_name": attr_name,
                "ui_data_attr": ui_data_attr,
                "is_ui_data": is_ui_data,
                "found_value": found_value
            }
        )

        return found_value

    @staticmethod
    def _get_group_value(operator_instance, operator_type) -> Any:
        data_object = utils.resolve_data_object(operator_instance.data_path)
        group_data = operator_type.group_data_manager.get_group_data(data_object)
        operator_instance.group = group_data.get_group_name(operator_instance.name)
        found_value = operator_instance.group

        return found_value

    @staticmethod
    def _get_ui_data_value(attr_name: str, ui_data, ui_data_attr: str | None) -> Any:
        # The field has a ui_data_attr tag
        default_value = consts.DEFAULT_DESCRIPTION if ui_data_attr == "description" else None
        found_value = ui_data.setdefault(ui_data_attr, default_value)

        # Ensure that arrays are returning a list and not a single value and is not for subtypes
        # Only apply this conversion for array types (default_array)
        if (not isinstance(found_value, list)
                and attr_name == "default_array"):
            found_value = [found_value, found_value, found_value]

        return found_value

    @staticmethod
    def _get_overridable_library_value(operator_instance) -> bool:
        data_object = utils.resolve_data_object(operator_instance.data_path)

        # Use bracket notation for property path
        prop_path = f'["{operator_instance.name}"]'
        operator_instance.is_property_overridable_library = data_object.is_property_overridable_library(prop_path)
        found_value = operator_instance.is_property_overridable_library

        return found_value

    @staticmethod
    def _get_python_value(operator_instance) -> str:
        """Get PYTHON property value as a JSON string for editing."""
        data_object = utils.resolve_data_object(operator_instance.data_path)
        value = data_object[operator_instance.name]

        # Convert IDPropertyGroup to dict, then to JSON string (compact format)
        if type(value).__name__ == consts.PropertyTypes.ID_PROPERTY_GROUP:
            return json.dumps(dict(value))

        return "{}"