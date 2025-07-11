from . import utils, config

def draw_panel(self, context, data_path):
    """
    Flexible draw function that works with different context types

    Args:
        :param data_path: String path to the data object (e.g., "view_layer", "scene")
        :param context:
        :param self:
    """
    layout = self.layout

    # Get the data object dynamically
    data_object = utils.resolve_data_object(context, data_path)
    if not data_object:
        layout.label(text = f"No {data_path} available")
        return

    # Check if there are any properties to draw
    if not hasattr(data_object, config.ATTR_KEYS) or not len(data_object.keys()) > 0:
        return

    # Draw property buttons
    draw_prop_buttons(layout, data_path)
    layout.separator()

    # Retrieve all custom properties for the panel


    # Convert all properties to CPM format while linking to original property


    # Group properties by type
    regular_props = []
    cpm_groups = {}

    # Draw all cpm properties
    if hasattr(data_object, "cpm") and len(data_object.cpm) > 0:
        utils.add_property(True, data_object)

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
        utils.draw_property_row(
            layout,
            data_object,
            data_path,
            key,
            False)

    # Draw CPM groups as expandable sections
    for group_name, group_keys in cpm_groups.items():
        utils.draw_property_group(
            layout,
            data_object,
            data_path,
            group_name,
            group_keys)

def draw_prop_buttons(layout, data_path):
    # Draw the original "New" button
    new_prop_op = layout.operator(
        config.WM_PROPERTIES_ADD,
        text = "New",
        icon = config.ADD_ICON)
    new_prop_op.data_path = data_path

    # Draw the "New Group" button
    new_prop_group_op = layout.operator(
        config.CPM_ADD_NEW_PROPERTY_GROUP,
        text ="New Group",
        icon = config.ADD_ICON)
    new_prop_group_op.data_path = data_path