import json
import logging
from datetime import datetime, timezone

from ..entities import LogLevel

class StructuredLogger:
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create structured formatter
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = StructuredFormatter()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(self, level: LogLevel, message: str, **kwargs):
        """Log with structured context"""
        extra = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": kwargs
        }
        self.logger.log(
            level = level.value,
            msg = message,
            extra = extra,
            stacklevel = 2
        )

class StructuredFormatter(logging.Formatter):
    def format(self, record) -> str:
        log_entry = {
            "timestamp": getattr(record, "timestamp", datetime.now(timezone.utc).isoformat()),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        timestamp = getattr(record, "timestamp", datetime.now(timezone.utc).isoformat())
        context = getattr(record, "context", {})
        context_str = f" | {context}" if context else ""

        if hasattr(record, "context"):
            log_entry.update(record.context)

        return (f"CPM: [{record.levelname}] {timestamp}:\n"
                f"    {record.module}.{record.funcName}:{record.lineno}, "
                f"message: {record.getMessage()}{context_str}")