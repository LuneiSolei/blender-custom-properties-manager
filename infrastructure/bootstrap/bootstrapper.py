import bpy
from bpy.app.handlers import persistent
from .di_container import DIContainer
from ...application.services import (
    EditPropertyService,
    PropertyDataService,
    FieldService,
    GroupDataService
)
from ...shared import blender_panels
from ...core import original_draws, expand_states
from ...infrastructure.ui import draw_panels

di_container = DIContainer()

def register_services():
    di_container.register_singleton("property_data_service", PropertyDataService)
    di_container.register_singleton("field_service", FieldService)
    di_container.register_singleton("edit_property_service", EditPropertyService)
    di_container.register_singleton("group_data_service", GroupDataService)

def register_classes(classes: set):
    """
    Register classes for Blender.
    :param classes: Set of classes to be registered.
    """

    for cls in classes:
        # Ensure there are no duplicates
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)

def register_handlers():
    # Ensure we don't have any duplicates
    unregister_handlers()
    bpy.app.handlers.save_pre.append(serialize_on_pre_save)
    bpy.app.handlers.load_post.append(deserialize_on_post_load)

def register_draw_functions():
    for panel in blender_panels.panels:
        if hasattr(bpy.types, panel.name):
            panel_class = getattr(bpy.types, panel.name)
            original_draws[panel.name] = panel_class.draw
            panel_class.draw = _create_draw_function(panel.data_path)

def unregister_draw_functions():
    for panel_name, original_draw in original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw_panels = original_draw

def clear_state():
    original_draws.clear()
    expand_states.clear()

def unregister_classes(classes: set):
    for cls in classes:
        bpy.utils.unregister_class(cls)

def unregister_handlers():
    if serialize_on_pre_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(serialize_on_pre_save)

    if deserialize_on_post_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(deserialize_on_post_load)

def _create_draw_function(data_path: str):
    def draw_function(self, context):
        return draw_panels(self, context, data_path)

    return draw_function

# Handlers for Group Data serialization
@persistent
def deserialize_on_post_load(dummy):
    di_container.get("group_data_service").deserialize()

@persistent
def serialize_on_pre_save(dummy):
    di_container.get("group_data_service").serialize()
    pass