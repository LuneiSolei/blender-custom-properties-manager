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
    SUBTYPE = "subtype"
    SUBTYPE_ARRAY = "subtype_array"
    MIN = "min"
    MAX = "max"
    USE_SOFT_LIMITS = "use_soft_limits"
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
    FieldNames.SUBTYPE.value: FieldConfig(
        attr_prefix = "subtype_",
        draw_on = ['FLOAT', 'INT'],
        label = "Subtype",
        name = FieldNames.SUBTYPE.value,
    ),
    FieldNames.SUBTYPE_ARRAY: FieldConfig(
        attr_prefix = "subtype_array_",
        draw_on = ['FLOAT_ARRAY', 'INT_ARRAY'],
        label = "Subtype",
        name = FieldNames.SUBTYPE_ARRAY.value
    ),
    FieldNames.MIN.value: FieldConfig(
        attr_prefix = "min_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Min",
        name = FieldNames.MIN.value
    ),
    FieldNames.MAX.value: FieldConfig(
        attr_prefix = "max_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Max",
        name = FieldNames.MAX.value
    ),
    FieldNames.USE_SOFT_LIMITS.value: FieldConfig(
        attr_name = "use_soft_limits",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Use Soft Limits",
        name = FieldNames.USE_SOFT_LIMITS.value
    ),
    FieldNames.SOFT_MIN.value: FieldConfig(
        attr_prefix = "soft_min_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Soft Min",
        name = FieldNames.SOFT_MIN.value
    ),
    FieldNames.SOFT_MAX.value: FieldConfig(
        attr_prefix = "soft_max_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Soft Max",
        name = FieldNames.SOFT_MAX.value
    ),
    FieldNames.STEP.value: FieldConfig(
        attr_prefix = "step_",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY'],
        label = "Step",
        name = FieldNames.STEP.value
    ),
    FieldNames.PRECISION.value: FieldConfig(
        attr_name = "precision",
        draw_on = ['FLOAT', 'FLOAT_ARRAY'],
        label = "Precision",
        name = FieldNames.PRECISION.value
    )
}
