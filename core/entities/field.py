from typing import Any, Callable, List, Optional, Union
from .reporting_mixin import ReportingMixin
from ...shared import ALL

import bpy

class Field(ReportingMixin):
    name: str
    label: str
    draw_on: Union[str, List[str]]
    attr_prefix: Optional[str] = None
    ui_data_attr: Optional[str] = None
    attr_name: Optional[str] = None
    _current_value: Any = None

    def __init__(
            self, *,
            label: str,
            name: str,
            draw_on: Union[str, List[str]],
            attr_prefix: Optional[str] = None,
            ui_data_attr: Optional[str] = None,
            attr_name: Optional[str] = None,
            property_type: str
    ):
        super().__init__()
        self.label = label
        self.name = name
        self.draw_on = draw_on
        self.attr_prefix = attr_prefix
        self.ui_data_attr = ui_data_attr

        # UI data in Blender uses specific names for properties such as min_float, soft_max_int, etc. So, we need
        # to generate this name based off of our property's type
        self._generate_attr_name(attr_name, property_type)

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = value

    def draw(self, operator: bpy.types.Operator) -> bpy.types.UILayout:
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
        """Determine if the field should be drawn"""
        return property_type in self.draw_on or self.draw_on == ALL

    def _generate_attr_name(self, attr_name: str, property_type: str):
        if self.attr_prefix:
            self.attr_name = f"{self.attr_prefix}{property_type.lower()}"
            self.attr_name = self.attr_name.removesuffix("_array")
        else:
            self.attr_name = attr_name

    def apply(self, operator):
        # Format method name with "apply_" prefix
        method_name = f"apply_{self.attr_name}"

        # Call the method by name using the method's object
        method = getattr(self, method_name)
        method(operator)