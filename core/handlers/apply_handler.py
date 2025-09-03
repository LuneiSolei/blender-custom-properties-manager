from abc import ABC, abstractmethod
from ..entities.field import Field

class ApplyHandler(ABC):
    @abstractmethod
    def handle(self, field: Field, operator) -> None:
        pass