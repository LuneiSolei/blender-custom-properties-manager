from enum import EnumType
from typing import Optional, TypedDict, Union

class UIData(TypedDict, total = False):
    subtype: Optional[str]
    min: Optional[Union[float, int]]
    max: Optional[Union[float, int]]
    soft_min: Optional[Union[float, int]]
    soft_max: Optional[Union[float, int]]
    precision: Optional[int]
    step: Optional[float]
    default: Optional[Union[float, list[float], int, list[int], bool, list[bool], str]]
    id_type: Optional[str] # Used in data-blocks to specify which ID type (Object, Material, etc.)
    items: Optional[EnumType]
    description: Optional[str]