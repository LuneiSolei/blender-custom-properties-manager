from dataclasses import dataclass
from enum import Enum
from .. import ApplyHandler
from .. import ApplyNameHandler, ApplyGroupHandler, ApplyTypeHandler, ApplyMinHandler

@dataclass
class FieldConfig:
    name: str
    handler: ApplyHandler
    draw_on: str
    field_type: str
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
        field_type = 'TEXT',
        handler = ApplyNameHandler(),
        label = "Property Name",
        name = FieldNames.NAME.value,
    ),
    FieldNames.GROUP.value: FieldConfig(
        attr_name = "group",
        draw_on = 'ALL',
        field_type = 'TEXT',
        handler = ApplyGroupHandler(),
        label = "Group Name",
        name = FieldNames.GROUP.value
    ),
    FieldNames.TYPE.value: FieldConfig(
        attr_name = "type",
        draw_on = 'ALL',
        field_type = 'DROPDOWN',
        handler = ApplyTypeHandler(),
        label = "Type",
        name = FieldNames.TYPE.value
    ),
    FieldNames.MIN.value: FieldConfig(
        attr_prefix = "min_",
        draw_on = 'ALL',
        field_type = 'INT',
        handler = ApplyMinHandler(),
        label = "Min Value",
        name = FieldNames.MIN.value
    )
}