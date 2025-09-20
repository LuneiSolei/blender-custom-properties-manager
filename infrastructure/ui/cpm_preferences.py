import bpy

from ...shared import consts

class CPMPreferences(bpy.types.AddonPreferences):
    bl_idname = consts.ADDON_NAME

    # noinspection PyTypeHints
    show_debug_info: bpy.props.BoolProperty(
        name="Show Debug Info",
        description="Show debug information in the UI",
        default=False
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text = "Show Debug Info")
        layout.prop(self, "show_debug_info")