import bpy, json
from bpy.app.handlers import persistent

from . import config
from .core.state import cpm_state
from .core.property_group_data import PropertyGroupData
from .ui import panels
from .core import ops

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
    ops.AddNewPropertyGroupOperator,
    ops.ExpandToggleOperator,
    ops.EditPropertyPopupOperator
}

@persistent
def deserialize_on_post_load(dummy):
    all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
    for data_object in all_objects:
        data_str = data_object.get(config.CPM_SERIALIZED_GROUP_DATA,
                                   config.CPM_DEFAULT_GROUP_DATA)
        group_data = json.loads(data_str)
        new_data = PropertyGroupData(
            grouped = group_data.get("grouped", []),
            ungrouped = group_data.get("ungrouped", [])
        )

        new_data.verify(data_object)

@persistent
def serialize_on_pre_save(dummy):
    """Serialize CPM group data before saving"""

    all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
    for data_object in all_objects:
        group_data = PropertyGroupData.get_data(data_object)

        data_dict = {
            "grouped": group_data.grouped,
            "ungrouped": group_data.ungrouped
        }
        data_object[config.CPM_SERIALIZED_GROUP_DATA] = json.dumps(data_dict)

def _create_flexible_draw_function(data_path):
    """Factory function to create draw functions for different contexts"""
    def draw_function(self, context):
        return panels.draw(self, context, data_path)
    return draw_function

def register():
    # Register classes
    for cls in _classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)

    # Create custom draw functions
    for item in config.panels:
        if hasattr(bpy.types, item.name):
            panel_class = getattr(bpy.types, item.name)
            cpm_state.original_draws[item.name] = panel_class.draw
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
    for panel_name, original_draw in cpm_state.original_draws.items():
        if hasattr(bpy.types, panel_name):
            getattr(bpy.types, panel_name).draw = original_draw

    # Clear state storage
    cpm_state.original_draws.clear()
    cpm_state.expand_states.clear()

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