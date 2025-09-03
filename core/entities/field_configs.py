from dataclasses import dataclass
from enum import Enum
from ..handlers.apply_handler import ApplyHandler
from ..handlers.name_handler import ApplyNameHandler
from ..handlers.group_handler import ApplyGroupHandler
from ..handlers.type_handler import ApplyTypeHandler
from ..handlers.min_handler import ApplyMinHandler

@dataclass
class FieldConfig:
    name: str
    handler: ApplyHandler
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
        handler = ApplyNameHandler(),
        label = "Property Name",
        name = FieldNames.NAME.value,
    ),
    FieldNames.GROUP.value: FieldConfig(
        attr_name = "group",
        draw_on = 'ALL',
        handler = ApplyGroupHandler(),
        label = "Group Name",
        name = FieldNames.GROUP.value
    ),
    FieldNames.TYPE.value: FieldConfig(
        attr_name = "type",
        draw_on = 'ALL',
        handler = ApplyTypeHandler(),
        label = "Type",
        name = FieldNames.TYPE.value
    ),
    FieldNames.MIN.value: FieldConfig(
        attr_prefix = "min_",
        draw_on = 'ALL',
        handler = ApplyMinHandler(),
        label = "Min Value",
        name = FieldNames.MIN.value
    )
}