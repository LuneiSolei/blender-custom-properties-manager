import bpy
from typing import Union, Any, TYPE_CHECKING, Type, Callable


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

def blender_prop(
    type_hint: Type[Any],
    prop_class: Callable[..., Any],
    **kwargs: Any
) -> Any:
    """
    Helper to create a single Blender property with type checking.
        :param type_hint: The Python type for type checking (str, int, float, etc.).
        :param prop_class: The Blender property class (StringProperty,
            IntProperty, etc.).
        :param kwargs: Additional keyword arguments to pass to the Blender
            property constructor.
        :return:
            During TYPE_CHECKING: The type_hint for IDEs.
            During runtime: An instance of the prop_class.
    """
    return type_hint if TYPE_CHECKING else prop_class(**kwargs)

def get_ui_data(data_object: bpy.types.Object, prop_name: str) -> None:
    return data_object.id_properties_ui(prop_name).as_dict()

def get_properties(data_object: bpy.types.Object) -> None:
    return data_object.properties