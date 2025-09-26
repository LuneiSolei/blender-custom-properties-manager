import json

from typing import Any, Union
from ...core import Field, FieldNames, field_configs
from ...shared import consts, utils
from ...shared.utils import StructuredLogger
from ...shared.entities import LogLevel

class FieldManager:
    logger = StructuredLogger(consts.MODULE_NAME)

    @classmethod
    def setup_fields(cls, operator_instance, operator_type) -> str:
        """
        Sets up the relevant fields for an EditPropertyMenu operator_instance instance.

        :param operator_instance: The EditPropertyMenu operator_instance instance.
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
                    attr_name = new_field.attr_name,
                    ui_data_attr = new_field.ui_data_attr
                )

            fields[name] = new_field

        return FieldManager.stringify_fields(fields)

    @classmethod
    def stringify_fields(cls, fields: dict[str, Field]) -> str:
        """
        Convert a dictionary of fields to a JSON string.

        :param fields: A dictionary of fields to convert.

        :return: A JSON string representing the fields.
        """
        field_data = [field.to_dict() for field in fields.values()]

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
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Finding value for attribute name",
            extra = {"attr_name": attr_name,}
        )
        ui_data = operator_instance.ui_data

        if ui_data is None:
            ui_data = operator_type.property_data_manager.load_ui_data(operator_instance)
            operator_instance.ui_data = ui_data

        if ui_data_attr is not None:
            found_value = ui_data[ui_data_attr]
        elif attr_name == FieldNames.GROUP.value:
            # noinspection PyTypeChecker
            data_object = utils.resolve_data_object(operator_instance.data_path)
            group_data = operator_type.group_data_manager.get_group_data(data_object)
            operator_instance.group = group_data.get_group_name(operator_instance.name)
            found_value = operator_instance.group
        else:
            found_value = getattr(operator_instance, attr_name)

        return found_value