import bpy

from ...shared import consts

class CPMPreferences(bpy.types.AddonPreferences):
    bl_idname = consts.MODULE_NAME

    # noinspection PyTypeHints
    log_level: bpy.props.EnumProperty(
        items=consts.LOG_LEVELS,
        name = "Log Level",
        description = "Level of debug information to display",
        default = consts.LOG_LEVELS[0][0]
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "log_level")