import bpy
from .. import config

#noinspection PyTypeHints
class AddNewPropertyGroupOperator(bpy.types.Operator):
    bl_label = "New Group"
    bl_idname = config.CPM_ADD_NEW_PROPERTY_GROUP_OP
    bl_description = "Add a new custom property group"
    bl_options = {'REGISTER', 'UNDO'}

    data_path: bpy.props.StringProperty(
        name = "Data Path",
        description = "Path to the target object",
        default = "Object")

    def execute(self, context):
        target = getattr(bpy.types, self.data_path)
        target["my_property"] = 1.0
        self.report({'INFO'}, "Added new custom property group")

        return {'FINISHED'}