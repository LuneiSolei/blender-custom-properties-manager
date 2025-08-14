# Property Fields
from collections import namedtuple

Field = namedtuple("Field", [
    "id",
    "label",
    "attr_prefix",
    "ui_data_attr",
    "attr_name",
    "draw_on"])
fields = [ # Fields are drawn in the order they are listed here
    Field(
        id = "name",
        label = "Property Name",
        attr_prefix = None,
        ui_data_attr = None,
        attr_name = "property_name",
        draw_on = 'ALL'),
    Field(
        id = "group",
        label = "Group Name",
        attr_prefix = None,
        ui_data_attr = None,
        attr_name = "group_name",
        draw_on = 'ALL'
    ),
    Field(
        id = "type",
        label = "Type",
        attr_prefix = None,
        ui_data_attr = None,
        attr_name = "type",
        draw_on = 'ALL'),
    Field(
        id = "value",
        label = "Value",
        attr_prefix = "value_",
        ui_data_attr = None,
        attr_name = None,
        draw_on = 'ALL'
    ),
    Field(
        id = "default",
        label = "Default",
        attr_prefix = "default_",
        ui_data_attr = "default",
        attr_name = None,
        draw_on = 'ALL'),
    Field(
        id = "min",
        label = "Min",
        attr_prefix = "min_",
        ui_data_attr = "min",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY']),
    Field(
        id = "max",
        label = "Max",
        attr_prefix = "max_",
        ui_data_attr = "max",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY']),
    Field(
        id = "soft_limits",
        label = "Soft Limits",
        attr_prefix = None,
        ui_data_attr = None,
        attr_name = "use_soft_limits",
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY']
    ),
    Field(
        id = "soft_min",
        label = "Soft Min",
        attr_prefix = "soft_min_",
        ui_data_attr = "soft_min",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY']
    ),
    Field(
        id = "soft_max",
        label = "Soft Max",
        attr_prefix = "soft_max_",
        ui_data_attr = "soft_max",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY']
    ),
    Field(
        id = "step",
        label = "Step",
        attr_prefix = "step_",
        ui_data_attr = "step",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY']
    ),
    Field(
        id = "precision",
        label = "Precision",
        attr_prefix = "precision_",
        ui_data_attr = "precision",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY']
    ),
    Field(
        id = "subtype",
        label = "Subtype",
        attr_prefix = "subtype_",
        ui_data_attr = "subtype",
        attr_name = None,
        draw_on = ['FLOAT', 'FLOAT_ARRAY']
    ),
    Field(
        id = "description",
        label = "Description",
        attr_prefix = None,
        ui_data_attr = "description",
        attr_name = "description",
        draw_on = 'ALL'
    ),
    Field(
        id = "library_overridable",
        label = "Library Overridable",
        attr_prefix = None,
        ui_data_attr = None,
        attr_name = "is_overridable_library",
        draw_on = 'ALL'
    )
]