import bpy

from ...core import expand_states
from ...shared import ops

# noinspection PyTypeHints
class ExpandToggleOperator(bpy.types.Operator):
    """Toggle expand/collapse state for property groups"""
    bl_idname = ops.CPM_EXPAND_TOGGLE
    bl_label = "Toggle Expand"
    bl_description = "Toggle the expand/collapse state of a property group"
    expand_key: bpy.props.StringProperty(
        name="Expand Key",
        description="Unique key for this expand state")
    current_state: bpy.props.BoolProperty(
        name="Current State",
        description="Current expand/collapse state")

    def execute(self, context):
        expand_states[self.expand_key] = not self.current_state

        return {'FINISHED'}