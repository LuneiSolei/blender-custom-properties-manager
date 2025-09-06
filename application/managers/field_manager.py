from typing import Any
from ...core import Field, field_configs, FieldNames
from .group_data_manager import GroupDataManager

class FieldManager:

    def __init__(self):
        pass

    def setup_fields(self, operator) -> dict:
        fields = {}

        # Populate fields with pre-defined configs
        for field_name in field_configs:
            field_config = field_configs[field_name]
            new_field = Field(
                **vars(field_config),
                property_type = operator.type
            )
            new_field.current_value = self.find_value(operator = operator, attr_name = new_field.attr_name)
            fields[field_name] = new_field

        return fields

    def find_value(self, operator, attr_name: str) -> Any:
        if attr_name in operator.ui_data:
            return operator.ui_data[attr_name]
        elif attr_name == FieldNames.GROUP:
            # noinspection PyTypeChecker
            # TODO: Use a service for GroupData
            operator.group = GroupDataManager.get_data(operator.data_object).get_group_name(operator.name)
            return operator.group

        return getattr(operator, attr_name)