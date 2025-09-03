from .di_container import DIContainer
from ..application.services import (
    EditPropertyService,
    ValidatePropertyService,
    EditPropertyNameService,
    PropertyDataService
)

# Register all services for the DI container
di_container = DIContainer()
di_container.register_singleton("edit_property_service", EditPropertyService)
di_container.register_singleton("validate_property_service", ValidatePropertyService)
di_container.register_singleton("property_data_service", PropertyDataService)
di_container.register_singleton("edit_property_name_service", EditPropertyNameService)