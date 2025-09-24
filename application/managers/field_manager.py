import json
from typing import Any

from ...shared.entities import LogLevel
from ...core import Field, field_configs, FieldNames
from ...shared import utils
from ...shared.utils import log_method

class FieldManager:
    def __init__(self):
        pass

    @staticmethod
    @log_method
    def setup_fields(operator_instance, operator_type) -> str:
        """
        Sets up the relevant fields for an EditPropertyMenu operator instance.

        :param operator_instance: The EditPropertyMenu operator instance.
        :param operator_type: The EditPropertyMenu type.

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
                new_field.current_value = FieldManager.find_value(
                    operator_instance = operator_instance,
                    operator_type = operator_type,
                    attr_name = new_field.attr_name
                )

            fields[name] = new_field

        return FieldManager.stringify_fields(fields)

    @staticmethod
    @log_method
    def stringify_fields(fields: dict[str, Field]) -> str:
        """
        Convert a dictionary of fields to a JSON string.

        :param fields: A dictionary of fields to convert.

        :return: A JSON string representing the fields.
        """
        field_data = [field.to_dict() for field in fields.values()]

        return json.dumps(field_data)

    @staticmethod
    @log_method
    def load_fields(fields: str) -> dict[str, Field]:
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

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Loaded {len(return_value)} fields: {list(return_value.keys())}"
        )

        return return_value

    @staticmethod
    @log_method
    def find_value(operator_instance, operator_type, attr_name: str) -> Any:
        """
        Find the value in the operator_instance based on the attr_name.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param operator_type: The Blender type of the operator_instance.
        :param attr_name: The name of the attribute to find the value of.

        :return: The value of the attribute.
        """
        ui_data = operator_instance.ui_data
        found_value = attr_name

        if ui_data is None:
            ui_data = operator_type.property_data_manager.load_ui_data(operator_instance)
            operator_instance.ui_data = ui_data

        if attr_name in ui_data:
            found_value = ui_data[attr_name]
        elif attr_name == FieldNames.GROUP:
            # noinspection PyTypeChecker
            data_object = utils.resolve_data_object(operator_instance.data_path)
            group_data = operator_type.group_data_manager.get_group_data(data_object)
            operator_instance.group = group_data.get_group_name(operator_instance.name)

            found_value = operator_instance.group

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Field '{attr_name}' resolved to value: {found_value}"
        )

        return getattr(operator_instance, found_value)