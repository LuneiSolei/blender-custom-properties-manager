from .field import Field

class TextField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)