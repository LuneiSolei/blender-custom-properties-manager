import bpy

from ...shared import consts
from ...application.managers import PreferencesManager

class CPMPreferences(bpy.types.AddonPreferences):
    bl_idname = consts.MODULE_NAME

    # noinspection PyTypeHints
    log_level: bpy.props.EnumProperty(
        items=consts.LOG_LEVELS,
        name = "Log Level",
        description = "Level of debug information to display",
        default = consts.LOG_LEVELS[0][0],
        update = PreferencesManager.on_log_level_update
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "log_level")