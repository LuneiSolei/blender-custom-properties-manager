import bpy
from collections import namedtuple
from . import ops, panels, utils, props

"""
CPMProperty(PropertyGroup) {
    prop_name: StringProperty()
    group_name: StringProperty() # None if null

    # Property Values
    
}
"""

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

def register():
    global original_draws

    # Register classes
    bpy.utils.register_class(props.CPMProperty)
    bpy.utils.register_class(ops.AddNewPropertyGroupOperator)
    bpy.utils.register_class(ops.ExpandToggleOperator)

    Panel = namedtuple("Panel", ["name", "data_path"])
    bl_panels = [
        Panel("VIEWLAYER_PT_layer_custom_props", "view_layer"),
        Panel("SCENE_PT_custom_props", "scene"),
        Panel("OBJECT_PT_custom_props", "active_object"),
        Panel("DATA_PT_custom_props_light", "active_object.data"),
    ]

    for panel in bl_panels:
        if hasattr(bpy.types, panel.name):
            panel_class = getattr(bpy.types, panel.name)
            original_draws[panel.name] = panel_class.draw
            panel_class.draw = utils.create_flexible_draw_function(panel.data_path)

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
    bpy.utils.unregister_class(ops.AddNewPropertyGroupOperator)
    bpy.utils.unregister_class(ops.ExpandToggleOperator)

if __name__ == "__main__":
    register()