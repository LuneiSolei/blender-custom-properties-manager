from typing import ItemsView, Iterator, KeysView, List, Tuple, ValuesView

import bpy
from ...shared import consts
from .reporting_mixin import ReportingMixin

class GroupData(ReportingMixin):
    _cached_data: dict[str, list[str]]
    _group_data_name: str

    def __init__(self, group_data: dict[str, list[str]] = None):
        """
        Initialize GroupData.
        :param group_data: A string representing the serialized group data.
        """

        # Remove ourselves from the property list to avoid recursion
        super().__init__()
        self._cached_data = group_data
        self._group_data_name = consts.CPM_SERIALIZED_GROUP_DATA
        if self._group_data_name in self:
            del self[self._group_data_name]

        if group_data is None:
            raise ValueError("Argument `group_data` cannot be empty.")

    def __delitem__(self, key) -> bool:
        """
        Removes the specified property from the group dataset.
        :param key: The name of the property to remove.
        :return: True if the property was removed, False otherwise.
        """
        for group, props in self._cached_data.items():
            if key in props:
                props.remove(key)
                return True

        return False

    def __getitem__(self, key: str) -> List[str]:
        """
        Get properties from the provided group.
        :param key: The name of the group.
        :return: List of properties in the group.
        """

        return self._cached_data.get(key, [])

    def __setitem__(self, key: str, value: List[str]) -> None:
        """
        Set a list of properties for a specific group.
        :param key: The group name.
        :param value: The list of properties to set for the provided group.
        """
        self._cached_data[key] = value

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over group names.
        :return: The iterator of group names.
        """
        return iter(self._cached_data)

    def __len__(self) -> int:
        """
        Get the number of groups.
        :return: The number of groups
        """
        return len(self._cached_data)
    
    def __contains__(self, item: str) -> bool:
        """
        Check if the group exists.
        :param item: The group name.
        :return: True if the group exists, False otherwise.
        """
        
        return item in self._cached_data

    def keys(self) -> KeysView[str]:
        """
        Get the iterator over group names.
        :return: The iterator over group names.
        """

        return self._cached_data.keys()

    def items(self) -> ItemsView[str, list[str]]:
        """
        Get the iterator over (group_name, props) pairs.
        :return: The iterator of (group_name, props) tuples.
        """

        return self._cached_data.items()

    def values(self) -> ValuesView[List[str]]:
        """
        Get the iterator over the list of properties in each group.
        :return: The iterator over the lists of properties.
        """

        return self._cached_data.values()

    def get_group_properties(self, key: str, default = None) -> List[str]:
        """
        Get properties for a group with a default if the group doesn't exist.
        :param key: The group name.
        :param default: The default value to return if the group doesn't exist.
        :return: A list of properties or the default.
        """

        return self._cached_data.get(key, default)

    def as_dict(self) -> dict[str, list[str]]:
        return self._cached_data.copy()

    def update_property_name(self, *, data_object: bpy.types.Object, prop_name: str, new_name: str):
        """
        Updates name of the property.

        :param data_object: Blender data object the property belongs to.
        :param prop_name: The name of the property to update.
        :param new_name: The new name of the property.
        """

        # Ensure property exists in any of the object's group data
        found = False
        for group, props in self._cached_data.items():
            if prop_name in props:
                index = props.index(prop_name)
                props[index] = new_name
                found = True
                break

        if not found:
            self.report({'ERROR'}, f"Property '{prop_name}' not found in '{data_object.name}'.")

    def update_property_group(self, *, prop_name: str, new_group: str):
        """
        Updates the group the property belongs to.

        :param prop_name: The name of the property to update.
        :param new_group: The name of the group to attach the property to.
        """
        # Remove property from the old group
        for group_name, props in self._cached_data.items():
            if prop_name in props:
                prop_index = props.index(prop_name)
                props.pop(prop_index)
                break

        # Place property into the new group
        if not new_group:
            return

        for group_name, props in self._cached_data.items():
            if group_name == new_group:
                props.append(prop_name)
                return

        # Group does not exist, create it
        self._cached_data[new_group] = [prop_name]

    def update_property_type(self, *, data_object: bpy.types.Object, prop_name: str, new_type: str):
        """Updates the property_type of the property."""
        pass

    def verify(self, data_object: bpy.types.Object):
        """
        Verifies the group data of the provided blender object. During this
        process, the cache is automatically updated.

        :param data_object: (bpy.types.Object) The blender object that
        will be synchronized.

        :return: None
        """

        # Clean up any unused properties from the group data
        # Retrieve properties to be removed
        data_object_keys = set(data_object.keys())
        keys_to_remove = []
        for group in self._cached_data.values():
            for prop in group:
                if prop not in data_object_keys or prop.startswith("_"):
                    keys_to_remove.append(prop)

        # Remove properties from GroupData
        for key in keys_to_remove:
            del self[key]

    def get_group_name(self, prop_name: str) -> str:
        for group_name, props in self._cached_data.items():
            if prop_name in props:
                return group_name

        # Property wasn't found in any group
        return ""

    def clear(self):
        self._cached_data.clear()