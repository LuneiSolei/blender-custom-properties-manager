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
            extra = extra
        )

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": getattr(record, "timestamp", datetime.now(timezone.utc).isoformat()),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "context"):
            log_entry.update(record.context)

        return json.dumps(log_entry)