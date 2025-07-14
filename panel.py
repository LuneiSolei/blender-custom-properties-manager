import bpy
from typing import Union
from .property_group_data import PropertyGroupData
from .state import cpm_state
from . import config

__all__ = ["draw_panel"]

"""
{
    "grouped": [
        "groupA": [
            "propertyA-1",
            "propertyA-2",
            "propertyA-3",  
        ],
        "groupB": [
            "propertyB-1",
            "propertyB-2",
            "propertyB-3",
        ],
        "groupC": [
            "propertyC-1",
            "propertyC-2",
            "propertyC-3",
        ]
    ],
    "ungrouped": [
        "propertyA",
        "propertyB",
        "propertyC",
    ]
}
"""

def draw_panel(self, context, data_path):
    """
    Draws the panel associated with the provided context type.

    Args:
        :param data_path: String path to the data object (e.g., "view_layer", "scene")
        :param context:
        :param self:
    """
    layout = self.layout

    # Get the data object dynamically
    data_object = _resolve_data_object(context, data_path)
    if not data_object:
        layout.label(text = f"No {data_path} available")
        return

    # Check if there are any properties to draw
    if not hasattr(data_object, config.ATTR_KEYS) or not len(data_object.keys()) > 0:
        return

    # Draw add buttons
    _draw_add_buttons(layout, data_path)
    layout.separator()

    # Get deserialized data (data is automatically verified)
    cpm_group_data = PropertyGroupData.get_data(data_object)

    # Draw properties based on associated group
    for group_name, props in cpm_group_data.grouped:
        for prop in props:
            _draw_property(layout, data_object, data_path, prop, group_name)

    # Draw ungrouped properties
    for prop in cpm_group_data.ungrouped:
        _draw_property(layout, data_object, data_path, prop, "")

def _resolve_data_object(context: bpy.context, data_path: str) -> Union[bpy.types.Object, None]:
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

def _draw_property(
        layout: bpy.types.UILayout,
        data_object: bpy.types.Object,
        data_path: str,
        prop_name: str,
        group_name: str):
    """
    Draws a property.
    Args:
        :param prop_name: String name of the property.
        :param group_name: String name of the group prop_name belongs to.
    """
    match group_name:
        case "":
            _draw_property_row(layout, data_object, data_path, prop_name)
        case dict(group):
            for prop, group_name in group:
                _draw_property_group(layout, data_object, data_path, prop_name,
                                     group_name)

def _draw_add_buttons(layout, data_path):
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

def _draw_property_row(layout, data_object, data_path, prop_name):
    """Draws a single property row."""
    row = layout.row()
    row.prop(data_object, f'["{prop_name}"]', text = prop_name)

    # Draw the "edit property" button
    edit_op = row.operator(
        config.WM_PROPERTIES_EDIT,
        text = "",
        icon = config.PREFERENCES_ICON,
        emboss = False)
    edit_op.property_name = prop_name
    edit_op.data_path = data_path

    # Draw the "remove property" button
    remove_op = row.operator(
        config.WM_PROPERTIES_REMOVE,
        text = "",
        icon = config.X_ICON,
        emboss = False
    )
    remove_op.property_name = prop_name
    remove_op.data_path = data_path

def _draw_property_group(
        layout: bpy.types.UILayout,
        data_object: bpy.types.Object,
        data_path: str,
        group_name: str,
        group_data: dict):
    """
    Draws a sub panel for a group of properties.
    Args:
        :param layout: Blender layout.
        :param data_object: Blender object.
        :param data_path: String path to the data object (e.g., "view_layer", "scene")
        :param group_name: String name of the group.
        :param group_data: Dictionary of the group's properties.
    """
    box = layout.box()
    header = box.row()

    # Create a unique key for this group to store the expand state
    expand_key = f"_cpm_{data_object.name}_{data_path}_{group_name}"
    is_expanded = cpm_state.expand_states.get(expand_key)

    toggle_op = header.operator(
        config.CPM_EXPAND_TOGGLE,
        text = group_name,
        icon = config.DOWNARROW_HLT_ICON if is_expanded
               else config.RIGHTARROW_ICON,
        emboss = False)
    toggle_op.expand_key = expand_key
    toggle_op.current_state = is_expanded

    # Only draw the group's contents if expanded
    if is_expanded:
        for key in group_data:
            _draw_property_row(layout, data_object, data_path, key)