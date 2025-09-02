from .apply_handler import ApplyHandler
from ...core import Field

class ApplyTypeHandler(ApplyHandler):
    def handle(self, field: Field, operator) -> None:
        pass