import bpy
from bpy.props import StringProperty
from . import panels as msp

class AddNewPropertyGroupOperator(bpy.types.Operator):
    bl_label = "New Group"
    bl_idname = "cpm.add_new_property_group"
    bl_description = "Add a new custom property group"
    bl_options = {'REGISTER', 'UNDO'}
    
    data_path: StringProperty(
        name = "Data Path",
        description = "Path to the target object",
        default = "Object"
    )

    def execute(self, context):
        target = getattr(bpy.types, self.data_path)
        target["my_property"] = 1.0
        self.report({'INFO'}, "Added new custom property group")

        return {'FINISHED'}

class ExpandToggleOperator(bpy.types.Operator):
    """Toggle expand/collapse state for property groups"""
    bl_idname = "cpm.expand_toggle"
    bl_label = "Toggle Expand"
    bl_description = "Toggle the expand/collapse state of a property group"

    expand_key: bpy.props.StringProperty(
        name = "Expand Key",
        description = "Unique key for this expand state"
    )
    current_state: bpy.props.BoolProperty(
        name = "Current State",
        description = "Current expand/collapse state"
    )

    def execute(self, context):
        msp.expand_states[self.expand_key] = not self.current_state

        return {'FINISHED'}