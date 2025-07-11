import bpy
from . import ops, config, panel, utils

bl_info = {
    "name": "Custom Properties Manager",
    "author": "Lunei Solei",
    "version": (0, 0, 1),
    "blender": (4, 4, 3),
    "category": "UI",
    "location": "Properties > View Layer > Custom Properties",
    "description": "Manage custom properties"
}

classes = {
    ops.AddNewPropertyGroupOperator,
    ops.ExpandToggleOperator
}

# Store original draw functions
original_draws = {}

def create_flexible_draw_function(data_path):
    """Factory function to create draw functions for different contexts"""
    def draw_function(self, context):
        return panel.draw_panel(self, context, data_path)
    return draw_function

def register():
    global original_draws

    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    for item in config.panels:
        if hasattr(bpy.types, item.name):
            panel_class = getattr(bpy.types, item.name)
            original_draws[item.name] = panel_class.draw
            panel_class.draw = create_flexible_draw_function(item.data_path)

def unregister():
    global original_draws

    # Restore all original draw functions
    for panel_name, original_draw in original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw = original_draw

    # Clear storage
    original_draws.clear()

    # Clear expand state storage
    utils.expand_states.clear()

    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()