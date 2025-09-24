import bpy, functools

from .. import consts
from ...shared.entities import LogLevel

def log(level: LogLevel, message: str):
    """Log a message if the level is enabled."""
    if _should_log(level):
        print(f"[CPM] '{level.name.capitalize()}': {message}")

def _get_log_level() -> LogLevel:
    """Helper to get the current log level from addon preferences."""
    prefs = bpy.context.preferences.addons[consts.MODULE_NAME].preferences

    return LogLevel(int(prefs.log_level))

def _should_log(level: LogLevel) -> bool:
    """Helper to determine if the message should be logged based on the current log level preference."""
    current_level = _get_log_level()

    return level.value >= current_level.value and current_level != LogLevel.NONE

def log_method(func):
    """Decorator that logs the starting and exiting of a method."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get class name if it's a method, otherwise use module name
        if args:
            # For class methods, args[0] is the class itself
            if isinstance(args[0], type):
                class_name = args[0].__name__
            elif hasattr(func, '__qualname__') and '.' in func.__qualname__:
                # For static methods, args[0] is the first parameter, but we want the class name from qualname
                class_name = func.__qualname__.rsplit('.', 1)[0]
            else:
                # For instance methods, args[0] is the instance
                class_name = args[0].__class__.__name__
        else:
            # For static methods or standalone functions with no args, try to get class from qualname
            if hasattr(func, '__qualname__') and '.' in func.__qualname__:
                class_name = func.__qualname__.rsplit('.', 1)[0]
            else:
                class_name = "Unknown"

        method_name = f"{class_name}.{func.__name__}"
        log(
            level = LogLevel.INFO,
            message = f"{method_name}: starting"
        )

        try:
            result = func(*args, **kwargs)
            log(
                level = LogLevel.INFO,
                message = f"{method_name}: completed successfully"
            )

            return result
        except Exception as e:
            log(
                level = LogLevel.ERROR,
                message = f"{method_name}: failed with {type(e).__name__}: {e}"
            )
            raise

    return wrapper