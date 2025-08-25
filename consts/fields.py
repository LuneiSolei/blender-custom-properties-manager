from dataclasses import dataclass

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
    "name": FieldConfig(
        attr_name = "name",
        draw_on = 'ALL',
        field_type = 'TEXT',
        label = "Property Name",
        name = "name"
    ),
    "group": FieldConfig(
        attr_name = "group",
        draw_on = 'ALL',
        field_type = 'TEXT',
        label = "Group Name",
        name = "group"
    ),
    "type": FieldConfig(
        attr_name = "type",
        draw_on = 'ALL',
        field_type = 'DROPDOWN',
        label = "Type",
        name = "type"
    )
}