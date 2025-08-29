from .field import Field

class TextField(Field):
    _current_value: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)