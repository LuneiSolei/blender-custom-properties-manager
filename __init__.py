import bpy
from collections import namedtuple
from . import operators
from . import panels
from . import properties
from . import utils

# CPMProperty(PropertyGroup) {
#   prop_name: StringProperty()
#   group_name: StringProperty() # None if null
# }

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
        return panels.custom_draw_function(self, context, data_path)
    return draw_function

def register():
    global original_draws

    # Register classes
    bpy.utils.register_class(properties.CPMProperty)
    bpy.utils
    bpy.utils.register_class(operators.AddNewPropertyGroupOperator)
    bpy.utils.register_class(operators.ExpandToggleOperator)

    Panel = namedtuple("Panel", ["name", "data_path"])
    panels = [
        Panel("VIEWLAYER_PT_layer_custom_props", "view_layer"),
        Panel("SCENE_PT_custom_props", "scene"),
        Panel("OBJECT_PT_custom_props", "active_object"),
        Panel("DATA_PT_custom_props_light", "active_object.data"),
    ]

    for panel in panels:
        if hasattr(bpy.types, panel.name):
            panel_class = getattr(bpy.types, panel.name)
            original_draws[panel.name] = panel_class.draw
            panel_class.draw = create_flexible_draw_function(panel.data_path)

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
    bpy.utils.unregister_class(operators.AddNewPropertyGroupOperator)
    bpy.utils.unregister_class(operators.ExpandToggleOperator)

if __name__ == "__main__":
    register()