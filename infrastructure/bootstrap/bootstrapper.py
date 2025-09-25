import bpy
from bpy.app.handlers import persistent
from .. import EditPropertyMenuOperator, AddPropertyGroupOperator, ExpandToggleOperator
from ...shared import consts
from ...core import original_draws, expand_states
from ..ui import draw_panels, CPMPreferences
from ...application.managers import GroupDataManager, PropertyDataManager, FieldManager

_classes = {
    AddPropertyGroupOperator,
    EditPropertyMenuOperator,
    ExpandToggleOperator,
    CPMPreferences
}

def register_classes():
    """Register entities for Blender."""

    for cls in _classes:
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
    for panel in consts.BLENDER_PANELS:
        if hasattr(bpy.types, panel.name):
            panel_class = getattr(bpy.types, panel.name)
            original_draws[panel.name] = panel_class.draw
            panel_class.draw = _create_draw_function(panel.data_path)

def unregister_draw_functions():
    for panel_name, original_draw in original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw = original_draw

def clear_state():
    original_draws.clear()
    expand_states.clear()

def unregister_classes():
    for cls in _classes:
        bpy.utils.unregister_class(cls)

def unregister_handlers():
    if serialize_on_pre_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(serialize_on_pre_save)

    if deserialize_on_post_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(deserialize_on_post_load)

def setup():
    EditPropertyMenuOperator.initialize(
        group_data_manager = GroupDataManager,
        property_data_manager = PropertyDataManager,
        field_manager = FieldManager
    )

def _create_draw_function(data_path: str):
    def draw_function(self, context):
        return draw_panels(self, context, data_path)

    return draw_function

# Handlers for Group Data serialization
@persistent
def deserialize_on_post_load(dummy):
    GroupDataManager.on_file_load()

@persistent
def serialize_on_pre_save(dummy):
    GroupDataManager.on_file_save()