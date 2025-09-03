from dataclasses import dataclass
from typing import Any, Dict, Optional

from ...core import Field
from .validate_property_service import ValidatePropertyService

@dataclass
class EditPropertyRequest:
    """Request object for property editing services"""
    object_name: str
    property_name: str
    property_type: str
    field_changes: Dict[str, Any]
    ui_data: Dict[str, Any]

@dataclass
class EditPropertyResponse:
    """Response object for property editing services"""
    success: bool
    updated_fields: Optional[Dict[str, Field]] = None
    error_message: Optional[str] = None
    validation_errors: Optional[Dict[str, str]] = None

class EditPropertyService:
    def __init__(self, validation_service: ValidatePropertyService):
        self._validation_service = validation_service