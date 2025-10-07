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
    MIN = "min_value"
    MAX = "max_value"
    USE_SOFT_LIMITS = "use_soft_limits"
    SOFT_MIN = "soft_min"
    SOFT_MAX = "soft_max"
    STEP = "step"
    PRECISION = "precision"
    DEFAULT = "default"
    PYTHON_VALUE = "python_value"
    IS_OVERRIDABLE_LIBRARY = "is_overridable_library"
    DESCRIPTION = "description"
    ARRAY_LENGTH = "array_length"
    ID_TYPE = "id_type"


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
    FieldNames.DESCRIPTION.value: FieldConfig(
        attr_name = "description",
        ui_data_attr = "description",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY', 'BOOL', 'BOOL_ARRAY', 'STRING', 'DATA_BLOCK'],
        label = "Description",
        name = FieldNames.DESCRIPTION.value
    ),
    FieldNames.TYPE.value: FieldConfig(
        attr_name = "property_type",
        draw_on = 'ALL',
        label = "Type",
        name = FieldNames.TYPE.value
    ),
    FieldNames.SUBTYPE.value: FieldConfig(
        attr_prefix = "subtype_",
        ui_data_attr = "subtype",
        draw_on = ['FLOAT', 'INT'],
        label = "Subtype",
        name = FieldNames.SUBTYPE.value,
    ),
    FieldNames.SUBTYPE_ARRAY.value: FieldConfig(
        attr_prefix = "subtype_array_",
        ui_data_attr = "subtype",
        draw_on = ['FLOAT_ARRAY', 'INT_ARRAY'],
        label = "Subtype",
        name = FieldNames.SUBTYPE_ARRAY.value
    ),
    FieldNames.ARRAY_LENGTH.value: FieldConfig(
        attr_name = "array_length",
        draw_on = ['FLOAT_ARRAY', 'INT_ARRAY', 'BOOL_ARRAY'],
        label = "Array Length",
        name = FieldNames.ARRAY_LENGTH.value
    ),
    FieldNames.DEFAULT.value: FieldConfig(
        attr_prefix = "default_",
        draw_on = ['FLOAT', 'INT', 'BOOL', 'STRING', 'FLOAT_ARRAY', 'INT_ARRAY', 'BOOL_ARRAY'],
        label = "Default",
        name = FieldNames.DEFAULT.value,
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
        ui_data_attr = "precision",
        draw_on = ['FLOAT', 'FLOAT_ARRAY'],
        label = "Precision",
        name = FieldNames.PRECISION.value
    ),
    FieldNames.PYTHON_VALUE.value: FieldConfig(
        attr_name = "default_python",
        draw_on = ['PYTHON'],
        label = "Value",
        name = FieldNames.PYTHON_VALUE.value
    ),
    FieldNames.ID_TYPE.value: FieldConfig(
        attr_name="id_type",
        ui_data_attr="id_type",
        draw_on=['DATA_BLOCK'],
        label="ID Type",
        name=FieldNames.ID_TYPE.value
    ),
    FieldNames.IS_OVERRIDABLE_LIBRARY.value: FieldConfig(
        attr_name = "is_property_overridable_library", # Needs to be called on bpy.types.ID, not the property itself
        draw_on = 'ALL',
        label = "Is Library Overridable",
        name = FieldNames.IS_OVERRIDABLE_LIBRARY.value
    )
}
