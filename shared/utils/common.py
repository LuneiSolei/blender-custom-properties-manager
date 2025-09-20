from typing import Union
from .. import consts

import bpy

def resolve_data_object(data_path: str) -> Union[bpy.types.Object, None]:
    """
    Resolve a data_path string to the actual object.

    :param data_path: String like "view_layer", "scene", "active_object.data", etc.

    :return: The resolved Blender object or None, if not found.
    """

    # Handle nested paths like "active_object.data"
    obj = bpy.context
    for attr in data_path.split("."):
        obj = getattr(obj, attr)
    return obj

def get_dynamic_blender_property(attr_type: str):
    types = {
        consts.PropertyTypes.FLOAT: bpy.props.FloatProperty,
        consts.PropertyTypes.FLOAT_ARRAY: bpy.props.FloatVectorProperty,
        consts.PropertyTypes.INT: bpy.props.IntProperty,
        consts.PropertyTypes.INT_ARRAY: bpy.props.IntVectorProperty,
        consts.PropertyTypes.BOOL: bpy.props.BoolProperty,
        consts.PropertyTypes.BOOL_ARRAY: bpy.props.BoolVectorProperty,
        consts.PropertyTypes.STRING: bpy.props.StringProperty,
        consts.PropertyTypes.PYTHON: bpy.props.StringProperty,
        consts.PropertyTypes.DATA_BLOCK: bpy.props.StringProperty
    }

    if attr_type in types:
        return types[attr_type]
    else:
        raise ValueError(f"{attr_type} is not a valid attribute property_type")

def get_blender_operator_type(bl_idname: str) -> bpy.types.Operator:
    """
    Convert a bl_idname string to Blender's generated class name as defined in bpy.types.

    :param bl_idname: The bl_idname string.

    :return: The Blender class name.
    """
    parts = bl_idname.split(".")
    bl_type: str
    if len(parts) == 2:
        category, operation = parts
        bl_type = f"{category.upper()}_OT_{operation}"
    else:
        # Fallback for unusual naming
        bl_type = bl_idname.replace(".", "_OT_").upper()

    return getattr(bpy.types, bl_type)