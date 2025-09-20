from typing import Any, Union

import bpy

def resolve_data_object(context, data_path: str) -> Union[bpy.types.Object, None]:
    """
    Resolve a data_path string to the actual object.
    Args:
        :param context: Blender context
        :param data_path: String like "view_layer", "scene", "active_object.data", etc.
    :return: The resolved object or None, if not found.
    """

    # Handle nested paths like "active_object.data"
    obj = context
    for attr in data_path.split("."):
        obj = getattr(obj, attr)
    return obj

def get_dynamic_blender_property(attr_type: str):
    types = {
        'FLOAT': bpy.props.FloatProperty,
        'FLOAT_ARRAY': bpy.props.FloatVectorProperty,
        'INT': bpy.props.IntProperty,
        'INT_ARRAY': bpy.props.IntVectorProperty,
        'BOOL': bpy.props.BoolProperty,
        'BOOL_ARRAY': bpy.props.BoolVectorProperty,
        'STRING': bpy.props.StringProperty,
        'PYTHON': bpy.props.StringProperty,
        'DATA_BLOCK': bpy.props.StringProperty
    }

    if attr_type in types:
        return types[attr_type]
    else:
        raise ValueError(f"{attr_type} is not a valid attribute type")

def on_type_change(self, context):
    """Called when the property type changes."""
    if not hasattr(self, "initialized") or not self.initialized:
        # Skip during initial setup
        return

    # Re-set up the fields with the new type
    if hasattr(self, "_field_manager"):
        # Save current values to restore after field setup
        current_values = {}
        for name, field in self.fields.items():
            current_values[name] = getattr(self, field.attr_name)

        # Set up fields for the new type
        self.fields = self._field_manager.setup_fields(self)

        # Restore previous values
        for attr_name, value in current_values.items():
            if hasattr(self, attr_name):
                setattr(self, attr_name, value)

        # Force redraw of the dialog
        self.refresh_ui(context)

# noinspection PyMethodMayBeStatic
def refresh_ui(self, context):
    """Forces a redrawing of the Edit Property Menu dialog"""
    for area in context.screen.areas:
        area.tag_redraw()