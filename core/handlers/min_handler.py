from .apply_handler import ApplyHandler
from ..entities.field import Field

class ApplyMinHandler(ApplyHandler):
    def handle(self, field: Field, operator) -> None:
        pass