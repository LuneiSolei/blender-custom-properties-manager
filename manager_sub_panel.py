import bpy

# Global storage for expand/collapse states
_expand_states = {}

def get_data_object(context, data_path):
    """
    Resolve a data_path string to the actual object

    Args:
        :param context: Blender context
        :param data_path: String like "view_layer", "scene", "active_object.data", etc.

    :return: The resolved object or None if not found
    """
    try:
        # Handle nested paths like "active_object.data"
        obj = context
        for attr in data_path.split("."):
            obj = getattr(obj, attr)
        return obj
    except AttributeError:
        return None

def custom_draw_function(self, context, data_path):
    """
    Flexible draw function that works with different context types

    Args:
        :param data_path: String path to the data object (e.g., "view_layer", "scene")
        :param context:
        :param self:
    """
    layout = self.layout

    # Get the data object dynamically
    data_object = get_data_object(context, data_path)
    if not data_object:
        layout.label(text = f"No {data_path} available")
        return

    # Draw the original "New" button
    new_prop_op = layout.operator("wm.properties_add", text = "New", icon = "ADD")
    new_prop_op.data_path = "view_layer"

    # TODO: Make this button work for all panels
    # Draw the "New Group" button
    new_prop_group_op = layout.operator("cpm.add_new_property_group", text = "New Group", icon = "ADD")
    new_prop_group_op.data_path = "view_layer"

    # Check if there are any properties to draw
    if not hasattr(data_object, 'keys') or not len(data_object.keys()) > 0:
        return

    layout.separator()

    # Group properties by type
    regular_props = []
    cpm_groups = {}

    # Draw all pre-existing properties
    for key in data_object.keys():
        # Skip any "private" properties
        if key.startswith("_"):
            continue

        if key.startswith("cpm."):
            # Group CPM properties
            cpm_name = key[4:]
            end_index = cpm_name.find(".")
            if end_index == -1:
                group_name = cpm_name
            else:
                group_name = cpm_name[:end_index]

            if group_name not in cpm_groups:
                cpm_groups[group_name] = []

            cpm_groups[group_name].append(key)
        else:
            regular_props.append(key)

    # Draw regular properties
    for key in regular_props:
        draw_property_row(layout, data_object, data_path, key, False)

    # Draw CPM groups as expandable sections
    for group_name, group_keys in cpm_groups.items():
        draw_property_group(layout, data_object, data_path, group_name, group_keys)


def draw_property_row(layout, data_object, data_path, key, group_child):
    """Helper function to draw a property row with edit/remove buttons"""
    row = layout.row()

    # Determine display name
    if not key.startswith("cpm."):
        # Common property
        display_name = key
    elif group_child:
        cpm_name = key[4:]
        start_index = cpm_name.find(".")
        if start_index == -1:
            display_name = key[4:]
        else:
            display_name = cpm_name[start_index + 1:]
    else:
        display_name = key[4:]

    row.prop(data_object, f'["{key}"]', text = display_name)

    # Draw the "edit property" button
    edit_op = row.operator("wm.properties_edit", text = "", icon = "PREFERENCES", emboss = False)
    edit_op.property_name = key
    edit_op.data_path = data_path

    # Draw the "remove property" button
    remove_op = row.operator("wm.properties_remove", text = "", icon = "X", emboss = False)
    remove_op.property_name = key
    remove_op.data_path = data_path

def draw_property_group(layout, data_object, data_path, group_name, group_keys):
    """Draw an expandable group of properties"""
    global _expand_states
    box = layout.box()

    # Header row with expand/collapse toggle
    header = box.row()

    # Create unique key for this group
    object_id = getattr(data_object, "name", str(id(data_object)))
    expand_key = f"_cpm_{data_path}_{object_id}_{group_name}"

    # Get current expand state (defaults to True)
    is_expanded = _expand_states.get(expand_key, True)

    # Create a toggle button
    toggle_op = header.operator("cpm.expand_toggle",
                                text = group_name,
                                icon = "DOWNARROW_HLT" if is_expanded else "RIGHTARROW",
                                emboss = False)
    toggle_op.expand_key = expand_key
    toggle_op.current_state = is_expanded

    # Only draw group contents if expanded
    if is_expanded:
        for key in group_keys:
            draw_property_row(box, data_object, data_path, key, True)