from ...shared.utils import StructuredLogger
from ...shared import consts

class PreferencesManager:
    @staticmethod
    def on_log_level_update(cpm_preferences, context):
        StructuredLogger(consts.MODULE_NAME, int(cpm_preferences.log_level))