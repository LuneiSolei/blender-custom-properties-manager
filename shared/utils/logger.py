import bpy

from .. import consts
from ...shared.classes import LogLevel


def _get_log_level() -> LogLevel:
    """Helper to get the current log level from addon preferences."""
    prefs = bpy.context.preferences.addons[consts.MODULE_NAME].preferences

    return LogLevel(int(prefs.log_level))

def _should_log(level: LogLevel) -> bool:
    """Helper to determine if the message should be logged based on the current log level preference."""
    current_level = _get_log_level()

    return level.value >= current_level.value

def log(message: str, level: LogLevel):
    """Log a message if the level is enabled."""
    if _should_log(level):
        print(f"[CPM] '{level.name.capitalize()}': {message}")