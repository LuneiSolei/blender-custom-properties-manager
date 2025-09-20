from dataclasses import dataclass
from enum import Enum
from typing import Union

@dataclass
class FieldConfig:
    name: str
    draw_on: Union[str, list[str]]
    label: str
    attr_name: str = ""
    attr_prefix: str = None
    ui_data_attr: str = None

class FieldNames(Enum):
    NAME = "name"
    GROUP = "group"
    TYPE = "property_type"
    MIN = "min"
    MAX = "max"
    SOFT_MIN = "soft_min"
    SOFT_MAX = "soft_max"
    STEP = "step"
    PRECISION = "precision"
    DEFAULT = "default"

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
        attr_name = "property_type",
        draw_on = 'ALL',
        label = "Type",
        name = FieldNames.TYPE.value
    ),
    FieldNames.MIN.value: FieldConfig(
        attr_prefix = "min_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Min Value",
        name = FieldNames.MIN.value
    ),
    FieldNames.MAX.value: FieldConfig(
        attr_prefix = "max_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Max Value",
        name = FieldNames.MAX.value
    ),
    FieldNames.SOFT_MIN.value: FieldConfig(
        attr_prefix = "soft_min_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Soft Min Value",
        name = FieldNames.SOFT_MIN.value
    ),
    FieldNames.SOFT_MAX.value: FieldConfig(
        attr_prefix = "soft_max_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Soft Max Value",
        name = FieldNames.SOFT_MAX.value
    )
}
