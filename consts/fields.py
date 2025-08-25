from dataclasses import dataclass
from enum import Enum

class FieldNames(Enum):
    NAME = "name"
    GROUP = "group"
    TYPE = "type"

@dataclass
class FieldConfig:
    attr_name: str = ""
    attr_prefix: str = ""
    draw_on: str = ""
    field_type: str = ""
    label: str = ""
    name: str = ""
    ui_data_attr: str = ""

fieldConfigs = {
    FieldNames.NAME.value : FieldConfig(
        attr_name = "name",
        draw_on = 'ALL',
        field_type = 'TEXT',
        label = "Property Name",
        name = FieldNames.NAME.value,
    ),
    FieldNames.GROUP.value: FieldConfig(
        attr_name = "group",
        draw_on = 'ALL',
        field_type = 'TEXT',
        label = "Group Name",
        name = FieldNames.GROUP.value
    ),
    FieldNames.TYPE.value: FieldConfig(
        attr_name = "type",
        draw_on = 'ALL',
        field_type = 'DROPDOWN',
        label = "Type",
        name = FieldNames.TYPE.value
    )
}