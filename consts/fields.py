from dataclasses import dataclass
from enum import Enum

ALL = 'ALL'

class FieldNames(Enum):
    NAME = "name"
    GROUP = "group"
    TYPE = "type"
    MIN = "min"

@dataclass
class FieldConfig:
    attr_name: str = ""
    attr_prefix: str = None
    draw_on: str = None
    field_type: str = None
    label: str = None
    name: str = None
    ui_data_attr: str = None

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
    ),
    FieldNames.MIN.value: FieldConfig(
        attr_prefix = "min_",
        draw_on = 'ALL',
        field_type = 'INT',
        label = "Min Value",
        name = FieldNames.MIN.value
    )
}