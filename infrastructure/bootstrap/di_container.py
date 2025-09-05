from typing import Callable

class DIContainer:
    def __init__(self):
        self._singleton_factories = {}
        self._singleton_instances = {}

    def register_singleton(self, name: str, factory: Callable):
        """
        Register a singleton service (created once, reused).
        :param name: Name of the singleton service.
        :param factory: Factory function that takes input data and returns an object reference.
        """

        self._singleton_factories[name] = factory

    def get(self, name: str):
        """
        Get a service by name.
        :param name: Name of the service.
        """
        # Check for singleton service
        if name in self._singleton_factories:
            # Return a cached instance if it exists
            if name in self._singleton_instances:
                return self._singleton_instances[name]

            # Create, cache, and return a new singleton instance
            instance = self._singleton_factories[name]()
            self._singleton_instances[name] = instance
            return instance
        # Service does not exist
        else:
            raise ValueError(f"Service '{name}' not registered")