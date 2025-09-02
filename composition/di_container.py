from typing import Callable

from ..application.services import EditPropertyService, ValidatePropertyService

class DIContainer:
    def __init__(self):
        self._singleton_factories = {}
        self._singleton_instances = {}
        self._transient_factories = {}

    def register_singleton(self, name: str, factory: Callable):
        """
        Register a singleton service (created once, reused).
        :param name: Name of the singleton service.
        :param factory: Factory function that takes input data and returns an object reference.
        """

        self._singleton_factories[name] = factory

    def register_transient(self, name: str, factory: Callable):
        """
        Register a transient service (always a new instance)
        :param name: Name of the transient service.
        :param factory: Factory function that takes input data and returns an object reference.
        """

        self._transient_factories[name] = factory

    def get(self, name: str):
        """
        Get a service by name.
        :param name: Name of the service.
        """
        # Check for singletons first
        if name in self._singleton_factories:
            # Return cached instance if it exists
            if name in self._singleton_instances:
                return self._singleton_instances[name]

            # Create, cache, and return new singleton instance
            instance = self._singleton_factories[name]()
            self._singleton_instances[name] = instance
            return instance

        # Check if it's a transient
        elif name in self._transient_factories:
            # Always create a new instance (no caching)
            return self._transient_factories[name]()

        # Service does not exist
        else:
            raise ValueError(f"Service '{name}' not registered")

def setup_container(container: DIContainer):
    """
    Setup container factories and instances.
    :param container: DIContainer in which to set up factories.
    """

    container.register_singleton("edit_property_service", EditPropertyService)
    container.register_singleton("validate_property_service", ValidatePropertyService)