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

def get_property_type_from_value(value: Any) -> str:
    """
    Gets the type of the property that the value represents.
    :rtype: str
    :param value: The value to get the type from.
    :return: The property's type as determined by Blender.
    """

    types = {
        "float": 'FLOAT',
        "float_array": 'FLOAT_ARRAY',
        "int": 'INT',
        "int_array": 'INT_ARRAY',
        "bool": 'BOOL',
        "bool_array": 'BOOL_ARRAY',
        "str": 'STRING',
        "IDPropertyGroup": 'PYTHON',
        "data_block": 'DATA_BLOCK'
    }
    prop_type = type(value).__name__

    if prop_type in types:
        # Property is of a standard type
        return types[prop_type]
    elif prop_type == "IDPropertyArray":
        # Property is of an array type
        has_values = len(value) > 0

        if has_values and isinstance(value[0], float):
            return types["float_array"]
        elif has_values and isinstance(value[0], int):
            return types["int_array"]
        elif has_values and isinstance(value[0], bool):
            return types["bool_array"]
        else:
            return types["float_array"]
    elif isinstance(value, bpy.types.ID):
        # Property is of a data_block type
        return types["data_block"]
    else:
        # Property type could not be determined. Theoretically, this should never happen
        return types["float"]