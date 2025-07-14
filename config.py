# This file defines all constants used to help avoid "magic strings"
from collections import namedtuple

# Configuration
DEBUG = False

# Window Manager Operators
WM_PROPERTIES_ADD = "wm.properties_add"
WM_PROPERTIES_REMOVE = "wm.properties_remove"
WM_PROPERTIES_EDIT = "wm.properties_edit"

# Icons
ADD_ICON = 'ADD'
PREFERENCES_ICON = 'PREFERENCES'
DOWNARROW_HLT_ICON = 'DOWNARROW_HLT'
RIGHTARROW_ICON = 'RIGHTARROW'
X_ICON = 'X'

# CPM Operators
CPM_EXPAND_TOGGLE = "cpm.expand_toggle"
CPM_ADD_NEW_PROPERTY_GROUP = "cpm.add_new_property_group"
CPM_ADD_NEW_PROPERTY = "cpm.add_new_property"

# Attributes
ATTR_KEYS = 'keys'

# Panels
Panel = namedtuple("Panel", ["name", "data_path"])
panels = [
    Panel("VIEWLAYER_PT_layer_custom_props", "view_layer"),
    Panel("SCENE_PT_custom_props", "scene"),
    Panel("OBJECT_PT_custom_props", "active_object"),
    Panel("DATA_PT_custom_props_light", "active_object.data"),
]

# Misc.
CPM_GROUP_DATA = "_cpm_group_data"
CPM_SERIALIZED_GROUP_DATA = "_cpm_serialized_group_data"
CPM_DEFAULT_GROUP_DATA = "{}"