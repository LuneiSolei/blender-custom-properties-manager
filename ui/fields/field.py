from abc import ABC
from typing import Any, List, Optional, Union
from ...consts import fields

import bpy

class Field(ABC):
    name: str
    label: str
    draw_on: Union[str, List[str]]
    attr_prefix: Optional[str] = None
    ui_data_attr: Optional[str] = None
    attr_name: Optional[str] = None

    _current_value: Any

    def __init__(
            self, *,
            label: str,
            name: str,
            draw_on: Union[str, List[str]],
            attr_prefix: Optional[str] = None,
            ui_data_attr: Optional[str] = None,
            attr_name: Optional[str] = None,
            current_value: Any,
            property_type: str
    ):
        self.label = label
        self.name = name
        self.draw_on = draw_on
        self.attr_prefix = attr_prefix
        self.ui_data_attr = ui_data_attr
        self._current_value = current_value

        self._generate_attr_name(attr_name, property_type)

    @property
    def current_value(self):
        """Returns the currently stored value of the field"""
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        """Sets the value of the field to be stored"""
        self._current_value = value

    def draw(self, operator: bpy.types.Operator) -> bpy.types.UILayout:
        layout = operator.layout
        row = layout.row()
        split = row.split(factor=0.5)

        # Create left column
        left_col = split.column()
        left_col.alignment = 'RIGHT'
        left_col.label(text = self.label)

        # Create right column
        right_col = split.column()
        right_col.prop(data = operator, property = self.attr_name, text="")

        return row

    def should_draw(self, property_type: str) -> bool:
        """Determine if the field should be drawn"""
        return property_type in self.draw_on or self.draw_on == fields.ALL

    def _generate_attr_name(self, attr_name: str, property_type: str):
        if self.attr_prefix:
            self.attr_name = f"{self.attr_prefix}{property_type.lower()}"
        else:
            self.attr_name = attr_name

    def apply_value(self):
        pass