import bpy
from typing import Union

def resolve_data_object(context: bpy.context, data_path: str) -> Union[
    bpy.types.Object, None]:
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