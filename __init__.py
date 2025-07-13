import bpy
from bpy.app.handlers import persistent
from . import ops, config, panel, serializer

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

@persistent
def serialize_all_cpm_data(dummy):
    """Serialize CPM group data before saving"""

    all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
    for data_object in all_objects:
        cpm_group_data = serializer.deserialize_object_cpm_group_data(data_object)
        cpm_group_data.cleanup(data_object)
        cpm_group_data.update(data_object)

        try:
            serializer.serialize_cpm_groups(data_object, cpm_group_data)
        except Exception as e:
            print(f"Failed to serialize CPM data for object {data_object.name}:"
                  f" {e}")

def create_flexible_draw_function(data_path):
    """Factory function to create draw functions for different contexts"""
    def draw_function(self, context):
        return panel.draw_panel(self, context, data_path)
    return draw_function

def register():
    global original_draws

    # Register classes
    for cls in classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)

    # Create custom draw functions
    for item in config.panels:
        if hasattr(bpy.types, item.name):
            panel_class = getattr(bpy.types, item.name)
            original_draws[item.name] = panel_class.draw
            panel_class.draw = create_flexible_draw_function(item.data_path)

    # Register Handlers
    if serialize_all_cpm_data in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(serialize_all_cpm_data)
    bpy.app.handlers.save_pre.append(serialize_all_cpm_data)

def unregister():
    # TODO: Remove all cpm properties from all objects
    global original_draws

    # Restore all original draw functions
    for panel_name, original_draw in original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw = original_draw

    # Clear storage
    original_draws.clear()

    # Clear expand state storage
    serializer.expand_states.clear()

    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()