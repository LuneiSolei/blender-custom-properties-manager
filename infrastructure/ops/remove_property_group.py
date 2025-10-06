import bpy

from bpy.props import StringProperty
from ...shared import consts, utils
from ...application.managers import GroupDataManager

# noinspection PyTypeHints
class RemovePropertyGroupOperator(bpy.types.Operator):
    """Remove a property group."""
    bl_idname = consts.ops.CPM_REMOVE_PROPERTY_GROUP
    bl_label = "Remove Property Group"
    bl_description = "Remove a property group"
    bl_options = {'REGISTER', 'UNDO'}

    data_path: StringProperty()
    group: StringProperty()

    @classmethod
    def initialize(cls, group_data_manager: type[GroupDataManager]):
        """Initialize the operator."""
        cls.group_data_manager = group_data_manager

    def execute(self, context):
        data_object = utils.resolve_data_object(self.data_path)
        self.group_data_manager.remove_property_group(data_object = data_object, group = self.group)

        # Force UI redraw
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}