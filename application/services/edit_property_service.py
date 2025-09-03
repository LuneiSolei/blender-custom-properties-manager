from .validate_property_service import ValidatePropertyService

class EditPropertyService:
    def __init__(self, validation_service: ValidatePropertyService):
        self._validation_service = validation_service