from abc import ABC
from typing import List, Optional, Union

class Field(ABC):
    name: str
    label: str
    draw_on: Union[str, List[str]] = "ALL"
    attr_prefix: Optional[str] = None
    ui_data_attr: Optional[str] = None
    attr_name: Optional[str] = None

    def __init__(
            self, *,
            name: str,
            label: str,
            draw_on: Union[str, List[str]],
            attr_prefix: Optional[str],
            ui_data_attr: Optional[str],
            attr_name: Optional[str]
    ):
        self.name = name
        self.label = label
        self.draw_on = draw_on
        self.attr_prefix = attr_prefix
        self.ui_data_attr = ui_data_attr
        self.attr_name = attr_name