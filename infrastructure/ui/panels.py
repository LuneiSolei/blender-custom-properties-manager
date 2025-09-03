import bpy

from itertools import chain
from ...core import utils
from ...core import GroupData
from ...shared import misc, ops, icons
from ...core import expand_states

def draw_panels(self, context, data_path):
    """
    Draws the panel associated with the provided context type.

    Args:
        :param data_path: String path to the data object (e.g., "view_layer", "scene")
        :param context:
        :param self:
    """
    layout = self.layout

    # Get the data object dynamically
    data_object = utils.resolve_data_object(context, data_path)
    if not data_object:
        layout.label(text=f"No {data_path} available")
        return

    # Check if there are any properties to draw
    if not hasattr(data_object, misc.KEYS_ATTR) or not len(data_object.keys()) > 0:
        return

    # Draw add buttons
    _draw_add_buttons(layout, data_path)
    layout.separator()

    # Get deserialized data (data is automatically verified)
    group_data = GroupData.get_data(data_object)

    # Draw properties based on associated group
    for group_name, props in chain.from_iterable(
            group.items() for group in group_data.grouped):
        _draw_property_group(
            layout,
            data_object,
            data_path,
            group_name,
            props)

    # Draw ungrouped properties
    for prop_name in group_data.ungrouped:
        _draw_property_row(
            layout,
            data_object,
            data_path,
            prop_name,
            group_name="")

def _draw_add_buttons(layout, data_path):
    # Draw the original "New" button
    new_prop_op = layout.operator(
        ops.WM_PROPERTIES_ADD,
        text = "New",
        icon=  icons.ADD)
    new_prop_op.data_path = data_path

    # Draw the "New Group" button
    new_prop_group_op = layout.operator(
        ops.CPM_ADD_PROPERTY_GROUP,
        text = "New Group",
        icon = icons.ADD)
    new_prop_group_op.data_path = data_path

def _draw_property_row(layout, data_object, data_path, prop_name, group_name):
    """Draws a single property row."""
    row = layout.row()

    # If the property's value is a list, draw a label manually. Otherwise,
    # Blender misbehaves and just shows the item count.
    if type(data_object[prop_name]) == list:
        row.label(text=prop_name)
    row.prop(data_object, f'["{prop_name}"]', text=prop_name)

    # Draw the "edit property" button
    edit_op = row.operator(
        ops.CPM_EDIT_PROPERTY,
        text = "",
        icon = icons.PREFERENCES,
        emboss=False)
    edit_op.name = prop_name
    edit_op.data_path = data_path
    edit_op.group = group_name

    # Draw the "remove property" button
    remove_op = row.operator(
        ops.WM_PROPERTIES_REMOVE,
        text = "",
        icon = icons.X,
        emboss=False
    )
    remove_op.property_name = prop_name
    remove_op.data_path = data_path

def _draw_property_group(
        layout: bpy.types.UILayout,
        data_object: bpy.types.Object,
        data_path: str,
        group_name: str,
        props: list):
    """
    Draws a sub panel for a group of properties.
    Args:
        :param layout: Blender layout.
        :param data_object: Blender object.
        :param data_path: String path to the data object (e.g., "view_layer", "scene")
        :param group_name: String name of the group.
        :param props: A list of the group's properties.
    """
    box = layout.box()
    header = box.row()

    # Create a unique key for this group to store the expand state
    expand_key = f"_cpm_{data_object.name}_{data_path}_{group_name}"
    is_expanded = expand_states.get(expand_key, True)

    toggle_op = header.operator(
        ops.CPM_EXPAND_TOGGLE,
        text=group_name,
        icon = icons.DOWNARROW_HLT if is_expanded
        else icons.RIGHTARROW,
        emboss=False)
    toggle_op.expand_key = expand_key
    toggle_op.current_state = is_expanded

    # Only draw the group's contents if expanded
    if is_expanded:
        for prop_name in props:
            _draw_property_row(box, data_object, data_path, prop_name,
                               group_name)