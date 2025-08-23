from abc import ABC, abstractmethod

from ..field import Field

class ArrayField(Field, ABC):
    def create(self, **kwargs):
        pass

    @abstractmethod
    def create_array_field(self, **kwargs):
        pass