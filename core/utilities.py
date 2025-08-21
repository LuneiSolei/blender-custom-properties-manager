import bpy
from typing import Union, Any
from .. import config


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

def get_property_type_from_value(value: Any) -> config.blender_property_types:
    """
    Gets the type of the property that the value represents.
    :param value: The value to get the type from.
    :return: The property's type as determined by Blender.
    """

    # Determine property type
    prop_type = type(value).__name__
    match prop_type:
        case "float":
            return 'FLOAT'
        case "int":
            return 'INT'
        case "bool":
            return 'BOOL'
        case "str":
            return 'STRING'
        case "IDPropertyArray":
            # Property is an array type
            if len(value) > 0:
                if isinstance(value[0], float):
                    return 'FLOAT_ARRAY'
                elif isinstance(value[0], int):
                    return 'INT_ARRAY'
                elif isinstance(value[0], bool):
                    return 'BOOL_ARRAY'
                else:
                    return 'FLOAT_ARRAY'
            else:
                return 'FLOAT_ARRAY'
        case "IDPropertyGroup":
            return 'PYTHON'
        case _ if isinstance(value, bpy.types.ID):
            return 'DATA_BLOCK'
        case _:
            return 'FLOAT'