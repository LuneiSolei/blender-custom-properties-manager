from dataclasses import dataclass
from enum import Enum
from typing import Callable

@dataclass
class FieldConfig:
    name: str
    draw_on: str
    label: str
    attr_name: str = ""
    attr_prefix: str = None
    ui_data_attr: str = None

class FieldNames(Enum):
    NAME = "name"
    GROUP = "group"
    TYPE = "type"
    MIN = "min"

field_configs = {
    FieldNames.NAME.value : FieldConfig(
        attr_name = "name",
        draw_on = 'ALL',
        label = "Property Name",
        name = FieldNames.NAME.value,
    ),
    FieldNames.GROUP.value: FieldConfig(
        attr_name = "group",
        draw_on = 'ALL',
        label = "Group Name",
        name = FieldNames.GROUP.value
    ),
    FieldNames.TYPE.value: FieldConfig(
        attr_name = "type",
        draw_on = 'ALL',
        label = "Type",
        name = FieldNames.TYPE.value
    ),
    FieldNames.MIN.value: FieldConfig(
        attr_prefix = "min_",
        draw_on = 'ALL',
        label = "Min Value",
        name = FieldNames.MIN.value
    )
}