from abc import ABC, abstractmethod
from ...core import Field

class ApplyHandler(ABC):
    @abstractmethod
    def handle(self, field: Field, operator) -> None:
        pass