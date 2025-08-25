from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union

class Field(ABC):
    name: str
    label: str
    cached_value: Any
    value: Any
    draw_on: Union[str, List[str]] = 'ALL'
    attr_prefix: Optional[str] = None
    ui_data_attr: Optional[str] = None
    attr_name: Optional[str] = None

    def __init__(
            self, *,
            label: str,
            name: str,
            cached_value: Any,
            value: Any,
            draw_on: Union[str, List[str]],
            attr_prefix: Optional[str],
            ui_data_attr: Optional[str],
            attr_name: Optional[str]
    ):
        self.label = label
        self.name = name
        self.cached_value = cached_value
        self.value = value
        self.draw_on = draw_on
        self.attr_prefix = attr_prefix
        self.ui_data_attr = ui_data_attr
        self.attr_name = attr_name

    @abstractmethod
    def set_value(self, value):
        pass