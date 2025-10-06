from ...shared import consts
from ...shared.utils import StructuredLogger

class PreferencesManager:
    @staticmethod
    def on_log_level_update(cpm_preferences, context):
        StructuredLogger(consts.MODULE_NAME, int(cpm_preferences.log_level))