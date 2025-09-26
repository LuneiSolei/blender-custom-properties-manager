from typing import Any, List, Optional, Union

import bpy

from .reporting_mixin import ReportingMixin
from .ui_data import UIData
from ...shared import consts

class Field(ReportingMixin):
    name: str
    label: str
    property_type: str
    draw_on: Union[str, List[str]]
    attr_prefix: Optional[str] = None
    ui_data_attr: Optional[str] = None
    attr_name: Optional[str] = None
    _current_value: Any = None

    def __init__(
            self, *,
            label: str,
            name: str,
            property_type: str,
            draw_on: Union[str, List[str]],
            attr_prefix: Optional[str] = None,
            ui_data_attr: Optional[str] = None,
            attr_name: Optional[str] = None
    ):
        super().__init__()
        self.label = label
        self.name = name
        self.draw_on = draw_on
        self.attr_prefix = attr_prefix
        self.ui_data_attr = ui_data_attr
        self.property_type = property_type

        # UI data in Blender uses specific names for properties such as min_float, soft_max_int, etc. So, we need
        # to generate this name based off of our property's property_type
        if attr_prefix is not None:
            self.attr_name = self._generate_attr_name()
            self.ui_data_attr = self._generate_ui_data_attr()
        else:
            self.attr_name = attr_name

    def to_dict(self) -> dict:
        """Convert the field to a serializable dictionary for JSON storage"""
        return {
            "name": self.name,
            "label": self.label,
            "property_type": self.property_type,
            "draw_on": self.draw_on,
            "attr_prefix": self.attr_prefix,
            "ui_data_attr": self.ui_data_attr,
            "attr_name": self.attr_name,
            "current_value": self.current_value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Field':
        """Construct a field from a dictionary"""
        field = cls(
            name = data["name"],
            label = data["label"],
            property_type = data["property_type"],
            draw_on = data["draw_on"],
            attr_prefix = data["attr_prefix"],
            ui_data_attr = data["ui_data_attr"],
            attr_name = data["attr_name"]
        )
        field.current_value = data["current_value"]
        return field

    @property
    def current_value(self):
        """Get the current value of the field"""
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        """Set the current value of the field"""
        self._current_value = value

    def draw(self, operator: bpy.types.Operator) -> bpy.types.UILayout:
        """Draw the field in the UI"""
        layout = operator.layout
        row = layout.row()
        split = row.split(factor=0.5)

        # Create the left column
        left_col = split.column()
        left_col.alignment = 'RIGHT'
        left_col.label(text = self.label)

        # Create the right column
        right_col = split.column()
        right_col.prop(data = operator, property = self.attr_name, text="")

        return row

    def should_draw(self, property_type: str) -> bool:
        """Helper to determine if the field should be drawn"""
        return property_type in self.draw_on or self.draw_on == consts.ALL

    def _generate_attr_name(self) -> str:
        """
        Helper to generate the attribute name based on the property type.

        :return: The generated attribute name.
        """
        return f"{self.attr_prefix}{self.property_type.lower()}".removesuffix("_array")

    def _generate_ui_data_attr(self) -> Union[str, None]:
        """
        Helper to generate the ui data name based on the attribute prefix.

        :return: The generated ui data attribute name.
        """
        search_str = self.attr_prefix.removesuffix("_")
        if hasattr(UIData, search_str):
            return search_str

        return None