import bpy
from . import operators as ops
from . import manager_sub_panel as msp

bl_info = {
    "name": "Custom Properties Manager",
    "author": "Lunei Solei",
    "version": (0, 0, 1),
    "blender": (4, 4, 3),
    "category": "UI",
    "location": "Properties > View Layer > Custom Properties",
    "description": "Manage custom properties"
}

# Store original draw functions
original_draws = {}

def create_flexible_draw_function(data_path):
    """Factory function to create draw functions for different contexts"""
    def draw_function(self, context):
        return msp.custom_draw_function(self, context, data_path)
    return draw_function

def register():
    global original_draws

    # Register classes
    bpy.utils.register_class(msp.ManagerSubPanel)
    bpy.utils.register_class(ops.AddNewPropertyGroupOperator)
    bpy.utils.register_class(ops.ExpandToggleOperator)

    # Override individual panel draw functions
    # View Layer panel
    if hasattr(bpy.types, "VIEWLAYER_PT_layer_custom_props"):
        original_draws["VIEWLAYER_PT_layer_custom_props"] = bpy.types.VIEWLAYER_PT_layer_custom_props.draw
        bpy.types.VIEWLAYER_PT_layer_custom_props.draw = create_flexible_draw_function("view_layer")

    # Scene panel
    if hasattr(bpy.types, "SCENE_PT_custom_props"):
        original_draws["SCENE_PT_custom_props"] = bpy.types.SCENE_PT_custom_props.draw
        bpy.types.SCENE_PT_custom_props.draw = create_flexible_draw_function("scene")

    # Object panel
    if hasattr(bpy.types, "OBJECT_PT_custom_props"):
        original_draws["OBJECT_PT_custom_props"] = bpy.types.OBJECT_PT_custom_props.draw
        bpy.types.OBJECT_PT_custom_props.draw = create_flexible_draw_function("active_object")

def unregister():
    global original_draws

    # Restore all original draw functions
    for panel_name, original_draw in original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw = original_draw

    # Clear storage
    original_draws.clear()

    # Clear expand state storage
    msp._expand_states.clear()

    # Unregister classes
    bpy.utils.unregister_class(msp.ManagerSubPanel)
    bpy.utils.unregister_class(ops.AddNewPropertyGroupOperator)
    bpy.utils.unregister_class(ops.ExpandToggleOperator)

if __name__ == "__main__":
    register()