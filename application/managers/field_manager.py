from typing import Any
from ...core import Field, field_configs, FieldNames
from .group_data_manager import GroupDataManager

class FieldManager:

    def __init__(self):
        pass

    @classmethod
    def setup_fields(cls, operator) -> dict:
        fields = {}

        # Populate fields with pre-defined configs
        for name, config in field_configs.items():
            new_field = Field(
                **vars(config),
                property_type = operator.type
            )

            if new_field.should_draw(operator.type):
                new_field.current_value = cls.find_value(operator = operator, attr_name = new_field.attr_name)

            fields[name] = new_field

        return fields

    @staticmethod
    def find_value(operator, attr_name: str) -> Any:
        if attr_name in operator.ui_data:
            return operator.ui_data[attr_name]
        elif attr_name == FieldNames.GROUP:
            # noinspection PyTypeChecker
            # TODO: Use a service for GroupData
            operator.group = GroupDataManager.get_data(operator.data_object).get_group_name(operator.name)
            return operator.group

        return getattr(operator, attr_name)