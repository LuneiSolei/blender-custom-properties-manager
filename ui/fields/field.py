from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union

class Field(ABC):
    name: str
    label: str
    draw_on: Union[str, List[str]] = 'ALL'
    attr_prefix: Optional[str] = None
    ui_data_attr: Optional[str] = None
    attr_name: Optional[str] = None

    def __init__(
            self, *,
            label: str,
            name: str,
            draw_on: Union[str, List[str]] = 'ALL',
            attr_prefix: Optional[str] = None,
            ui_data_attr: Optional[str] = None,
            attr_name: Optional[str] = None
    ):
        self.label = label
        self.name = name
        self.draw_on = draw_on
        self.attr_prefix = attr_prefix
        self.ui_data_attr = ui_data_attr
        self.attr_name = attr_name