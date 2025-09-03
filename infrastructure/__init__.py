from .di_container import DIContainer
from ..application.services import EditPropertyService, ValidatePropertyService, EditPropertyNameService

di_container = DIContainer()
di_container.register_singleton("edit_property_service", EditPropertyService)
di_container.register_singleton("validate_property_service", ValidatePropertyService)
di_container.register_singleton("edit_property_name_service", EditPropertyNameService)

__all__ = [
    "di_container"
]