from collections import namedtuple

FieldConfig = namedtuple(
    typename = "FieldConfig",
    field_names = [
        "field_type",
        "name",
        "label",
        "draw_on",
        "attr_prefix",
        "ui_data_attr",
        "attr_name"
    ]
)
fieldConfigs = [
    FieldConfig(
        field_type = 'STRING',
        name = "name",
        label = "Property Name",
        draw_on = "ALL",
        attr_prefix = None,
        ui_data_attr = None,
        attr_name = "name"
    )
]