from .di_container import DIContainer
from ..application.services import (
    EditPropertyService,
    PropertyDataService,
    FieldService
)

# Register all services for the DI container
di_container = DIContainer()
di_container.register_singleton("property_data_service", PropertyDataService)
di_container.register_singleton("field_service", FieldService)
di_container.register_singleton("edit_property_service", EditPropertyService)