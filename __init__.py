import bpy
from bpy.app.handlers import persistent

from .application import AddPropertyGroupOperator, EditPropertyMenuOperator, ExpandToggleOperator
from .application import draw_panels
from .shared import blender_panels
from .composition.di_container import DIContainer
from .core import GroupData, expand_states, original_draws

bl_info = {
    "name": "Custom Properties Manager",
    "author": "Lunei Solei",
    "version": (0, 0, 1),
    "blender": (4, 4, 3),
    "category": "UI",
    "location": "Properties > View Layer > Custom Properties",
    "description": "Manage custom properties"
}

_classes = {
    AddPropertyGroupOperator,
    EditPropertyMenuOperator,
    ExpandToggleOperator
}

@persistent
def deserialize_on_post_load(dummy):
    GroupData.deserialize()

@persistent
def serialize_on_pre_save(dummy):
    GroupData.serialize()

def _create_flexible_draw_function(data_path):
    """Factory function to create draw functions for different contexts"""

    def draw_function(self, context):
        return draw_panels(self, context, data_path)

    return draw_function

def register():
    container = DIContainer()

    # Register classes
    for cls in _classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)

    # Create custom draw functions
    for item in blender_panels.panels:
        if hasattr(bpy.types, item.name):
            panel_class = getattr(bpy.types, item.name)
            original_draws[item.name] = panel_class.draw
            panel_class.draw = _create_flexible_draw_function(item.data_path)

    # Register handlers
    if serialize_on_pre_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(serialize_on_pre_save)
    bpy.app.handlers.save_pre.append(serialize_on_pre_save)

    if deserialize_on_post_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(deserialize_on_post_load)
    bpy.app.handlers.load_post.append(deserialize_on_post_load)

def unregister():
    # Restore all original draw functions
    for panel_name, original_draw in original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw_panels = original_draw

    # Clear state storage
    original_draws.clear()
    expand_states.clear()

    # Unregister classes
    for cls in _classes:
        bpy.utils.unregister_class(cls)

    # Unregister handlers
    if serialize_on_pre_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(serialize_on_pre_save)

    if deserialize_on_post_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(deserialize_on_post_load)

if __name__ == "__main__":
    register()