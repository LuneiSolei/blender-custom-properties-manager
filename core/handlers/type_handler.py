from .apply_handler import ApplyHandler
from ..entities.field import Field

class ApplyTypeHandler(ApplyHandler):
    def handle(self, field: Field, operator) -> None:
        pass