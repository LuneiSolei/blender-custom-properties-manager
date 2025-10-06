import bpy

from typing import Any, List, Optional, Union, get_type_hints
from .reporting_mixin import ReportingMixin
from .ui_data import UIData
from ...shared import consts
from ...shared.utils import StructuredLogger
from ...shared.entities import LogLevel
from .field_configs import FieldNames

class Field(ReportingMixin):
    logger = StructuredLogger(consts.MODULE_NAME)
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
        has_prefix = attr_prefix is not None
        has_ui_data_attr = ui_data_attr is not None
        if has_prefix:
            self.attr_name = self._generate_attr_name()
        else:
            self.attr_name = attr_name

        if has_prefix and not has_ui_data_attr:
            self.ui_data_attr = self._generate_ui_data_attr()

    def as_dict(self) -> dict[str, str]:
        """
        Converts the field to a dictionary.

        :return: A dictionary representation of the field.
        """
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
        """
        Constructs a new Field instance from a dictionary representation.

        :param data: A dictionary representation of the field.

        :return: A new Field instance.
        """
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
        """Get the current value of the field."""
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        """Set the current value of the field."""
        self._current_value = value

    def draw(self, operator_instance: bpy.types.Operator) -> bpy.types.UILayout:
        """
        Draws the field in the provided operator_instance instance's layout.

        :param operator_instance: The operator_instance instance to draw on.

        :return: The row containing the field.
        """
        layout = operator_instance.layout
        row = layout.row()
        split = row.split(factor = 0.5)

        # Create the left column
        left_col = split.column()
        left_col.alignment = 'RIGHT'
        left_col.label(text = self.label)

        # Create the right column
        right_col = split.column()

        if (self.name == FieldNames.DEFAULT.value and
            operator_instance.property_type in [
                consts.PropertyTypes.FLOAT_ARRAY,
                consts.PropertyTypes.INT_ARRAY,
                consts.PropertyTypes.BOOL_ARRAY
            ]):
            self._draw_array_collection(operator_instance, right_col)
        elif self.attr_name != "default_array":
            # Only draw property if it's not the default_array collection
            right_col.prop(data = operator_instance, property = self.attr_name, text="")

        return row

    def should_draw(self, property_type: str) -> bool:
        """Determines if the field should be drawn."""
        return property_type in self.draw_on or self.draw_on == consts.ALL

    def _draw_array_collection(self, operator_instance, right_col):
        collection = operator_instance.default_array
        prop_type = operator_instance.property_type

        # Determine which value attribute to use
        value_attr_map = {
            consts.PropertyTypes.FLOAT_ARRAY: "float_value",
            consts.PropertyTypes.INT_ARRAY: "int_value",
            consts.PropertyTypes.BOOL_ARRAY: "bool_value"
        }

        value_attr = value_attr_map.get(prop_type)
        if not value_attr:
            return

        # Draw each element
        for i, element in enumerate(collection):
            right_col.prop(element, value_attr, text = f"[{i}]")

    def _generate_attr_name(self) -> str:
        """
        Helper to generate the attribute name based on the property type.

        :return: The generated attribute name.
        """
        return_str = f"{self.attr_prefix}{self.property_type.lower()}"
        if not self.attr_prefix == "default_":
            return return_str.removesuffix("_array")

        return return_str

    def _generate_ui_data_attr(self) -> Union[str, None]:
        """
        Helper to generate the ui data name based on the attribute prefix.

        :return: The generated ui data attribute name.
        """
        ui_data_attr = self.attr_prefix.removesuffix("_").removesuffix("_array")
        search_result = ui_data_attr in get_type_hints(UIData).keys()

        self.logger.log(
            level = LogLevel.DEBUG,
            message = "Generating UI data attribute name",
            extra = {
                "ui_data_attribute": ui_data_attr,
                "search_result": search_result
            }
        )

        if search_result:
            return ui_data_attr

        self.logger.log(
            level = LogLevel.WARNING,
            message = "Could not find UI data attribute name in UI data",
            extra = {
                "ui_data_attribute": ui_data_attr
            }
        )

        return None