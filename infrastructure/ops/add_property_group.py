import bpy
from ...shared import consts

# noinspection PyTypeHints
class AddPropertyGroupOperator(bpy.types.Operator):
    bl_label = "New Group"
    bl_idname = consts.ops.CPM_ADD_PROPERTY_GROUP
    bl_description = "Add a new custom property group"
    bl_options = {'REGISTER', 'UNDO'}

    data_path: bpy.props.StringProperty(
        name="Data Path",
        description="Path to the target object",
        default="Object")

    def execute(self, context):
        target = getattr(bpy.types, self.data_path)
        target["my_property"] = 1.0
        self.report({'INFO'}, "Added new custom property group")

        return {'FINISHED'}