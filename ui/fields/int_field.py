from .field import Field

class IntField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)