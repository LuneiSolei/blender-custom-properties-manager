from itertools import chain

import bpy

from ...application.managers import GroupDataManager
from ...core import expand_states
from ...shared import consts, utils

def draw_panels(panel: bpy.types.Panel, context, data_path: str):
    """
    Draws the panel associated with the provided context property_type.

    :param data_path: String path to the data object (e.g., "view_layer", "scene")
    :param context: The Blender context.
    :param panel: The panel to draw.
    """
    layout = panel.layout

    # Get the data object dynamically
    data_object = utils.resolve_data_object(data_path)
    if not data_object:
        return

    # Check if there are any properties to draw
    if not hasattr(data_object, consts.KEYS_ATTR) or not len(data_object.keys()) > 0:
        return

    # Draw add buttons
    _draw_add_buttons(layout, data_path)
    layout.separator()

    # Get deserialized data (data is automatically verified)
    group_data = GroupDataManager.get_group_data(data_object)

    # Draw properties based on the associated group
    lambda_sort = lambda x: x.lower()
    for group_name, props in group_data.items():
        props.sort(key = lambda_sort)
        _draw_property_group(
            layout,
            data_object,
            data_path,
            group_name,
            props
        )

    # Draw ungrouped properties
    grouped = sorted(set(chain.from_iterable(group_data.values())))
    ungrouped = sorted(set(data_object.keys()) - set(grouped), key = lambda_sort)
    for prop_name in ungrouped:
        _draw_property_row(
            layout,
            data_object,
            data_path,
            prop_name,
            group_name=""
        )

def _draw_add_buttons(layout, data_path):
    # Draw the original "New" button
    new_prop_op = layout.operator(
        consts.ops.WM_PROPERTIES_ADD,
        text = "New",
        icon=  consts.ADD)
    new_prop_op.data_path = data_path

    # Draw the "New Group" button
    # new_prop_group_op = layout.operator(
    #     consts.ops.CPM_ADD_PROPERTY_GROUP,
    #     text = "New Group",
    #     icon = consts.icons.ADD)
    # new_prop_group_op.data_path = data_path

def _draw_property_row(layout, data_object, data_path, prop_name, group_name):
    """Draws a single property row."""
    if prop_name.startswith("_"):
        # Skip private properties
        return

    row = layout.row()

    row.label(text = prop_name)
    row.prop(
        data = data_object,
        property = f'["{prop_name}"]',
        text = ""
    )

    # Draw the "edit property" button
    edit_op = row.operator(
        consts.ops.CPM_EDIT_PROPERTY,
        text = "",
        icon = consts.icons.PREFERENCES,
        emboss = False
    )
    edit_op.name = prop_name
    edit_op.data_path = data_path
    edit_op.group = group_name

    # Draw the "remove property" button
    remove_op = row.operator(
        consts.ops.WM_PROPERTIES_REMOVE,
        text = "",
        icon = consts.icons.X,
        emboss = False
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
    Draws a subpanel for a group of properties.
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
        consts.ops.CPM_EXPAND_TOGGLE,
        text = group_name,
        icon = consts.icons.DOWNARROW_HLT if is_expanded
            else consts.icons.RIGHTARROW,
        emboss = False)
    toggle_op.expand_key = expand_key
    toggle_op.current_state = is_expanded

    remove_group_op = header.operator(
        consts.ops.CPM_REMOVE_PROPERTY_GROUP,
        text = "",
        icon = 'TRASH',
        emboss = False)
    remove_group_op.data_path = data_path
    remove_group_op.group = group_name

    # Only draw the group's contents if expanded
    if is_expanded:
        for prop_name in props:
            _draw_property_row(box, data_object, data_path, prop_name, group_name)