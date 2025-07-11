import json
from . import config, props

# Global storage for expand/collapse states
expand_states = {}
cpm_groups = {}

def resolve_data_object(context, data_path):
    """
    Resolve a data_path string to the actual object.
    Args:
        :param context: Blender context
        :param data_path: String like "view_layer", "scene", "active_object.data", etc.
    :return: The resolved object or None, if not found.
    """
    try:
        # Handle nested paths like "active_object.data"
        obj = context
        for attr in data_path.split("."):
            obj = getattr(obj, attr)
        return obj
    except AttributeError:
        return None

def add_property(layout, data_object, data_path, prop):
    """The main draw method for custom properties"""
    if prop is None:
        return
    elif type(prop) is props.CPMProperty:
        draw_property_group(layout, data_object, data_path, prop.group_name)
    else:
        draw_property_row

def draw_property(layout, data_object, data_path, prop):
    return

def draw_cpm_prop(layout, data_object, data_path, cpm_prop):
    box = layout.box()
    header = box.row()

    expand_key = f"_cpm_{data_path}_{cpm_prop.group_name}"
    cpm_groups[f"cpm.{data_object}.{data_path}.{cpm_prop.group_name}"] = box

def draw_property_group(layout, data_object, data_path, group_name,
                         group_keys):
    """Draws a sub panel for a group of properties"""
    # Create a header row with expand toggle
    box = layout.box()
    header = box.row()

    # Create a unique key for this group
    expand_key = f"_cpm_{data_path}_{group_name}"
    cpm_groups[f"cpm.{data_object}.{data_path}.{group_name}"] = box

    is_expanded = expand_states.get(expand_key)
    toggle_op = header.operator(
        config.CPM_EXPAND_TOGGLE,
        text = group_name,
        icon = config.DOWNARROW_HLT_ICON if is_expanded
                else config.RIGHTARROW_ICON,
        emboss = False)
    toggle_op.expand_key = expand_key
    toggle_op.current_state = is_expanded

    # Only draw group contents if expanded
    if is_expanded:
        for key in group_keys:
            draw_property_row(box, data_object, data_path, key, True)

def draw_property_row(layout, data_object, data_path, key, use_cpm = False):
    """Draws a single property row"""
    row = layout.row()

    # Draw the property
    row.prop(data_object, f'["{key}"]', text = key)

    # Draw the "edit property" button
    edit_op = row.operator(
        config.WM_PROPERTIES_EDIT,
        text = "",
        icon = config.PREFERENCES_ICON,
        emboss = False)
    edit_op.property_name = key
    edit_op.data_path = data_path

    # Draw the "remove property" button
    remove_op = row.operator(
        config.WM_PROPERTIES_REMOVE,
        text = "",
        icon = config.X_ICON,
        emboss = False)
    remove_op.property_name = key
    remove_op.data_path = data_path

def get_property_group_layout(layout_key):
    if layout_key.startswith("cpm."):
        return cpm_groups[layout_key]
    else:
        return cpm_groups.get(f"cpm.{layout_key}")

def serialize_cpm_groups(obj, cpm_group_data):
    """Serializes grouping data for a specified object's custom properties"""
    if "grouped" and "ungrouped" in cpm_group_data:
        obj[config.CPM_SERIALIZED_GROUP_DATA] = json.dumps(cpm_group_data)

def deserialize_object_cpm_group_data(obj):
    """Load grouping data for a specified object's custom properties"""

    data_str = obj.get(config.CPM_SERIALIZED_GROUP_DATA, config.CPM_DEFAULT_GROUP_DATA)
    return json.loads(data_str)