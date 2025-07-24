import weakref

import bpy, json
from typing import Dict, Self
from .reporting_mixin import ReportingMixin
from .. import config

class GroupData(ReportingMixin):
    _cache = {}

    def __init__(self, grouped: list[Dict[str, list[str]]] = None,
                 ungrouped: list[str] = None, *args, **kwargs) -> None:
        """
        Initialize PropertyGroupData.

        :param grouped: A list of dictionaries describing groups with
        properties.
        :param ungrouped: A list of properties without groups.

        :return: None
        """
        super().__init__(*args, **kwargs)
        self.grouped = grouped if grouped is not None else []
        self.ungrouped = ungrouped if ungrouped is not None else []

        # Check if config.CPM_GROUP_DATA
        if config.CPM_GROUP_DATA in self:
            del self[config.CPM_GROUP_DATA]

    def __delitem__(self, prop_name) -> None:
        """
        Removes the specified property from the group dataset.

        :param prop_name: The name of the property to remove.

        :return: None
        """
        if prop_name in self.ungrouped:
            self.ungrouped.remove(prop_name)

        for group in self.grouped:
            for group_name, props in group.items():
                if prop_name in props:
                    props.remove(prop_name)

    def __contains__(self, prop_name: str) -> bool:
        """
        Checks if the property exists anywhere in the grouping dataset.

        :param prop_name: Name of the property to check.

        :return: True if the property exists, False otherwise.
        """
        # Check ungrouped data first
        if prop_name in self.ungrouped:
            return True

        return any(prop_name in props
                   for group in self.grouped
                   for props in group.values())

    def update_property_name(
        self,
        *,
        prop_name: str,
        new_name: str,
    ) -> None:
        """
        Updates the property name.

        :param prop_name: The name of the property to update.
        :param new_name: The new name of the property.
        """
        # Ensure property exists in group data
        if not prop_name in self:
            self.report({'ERROR'}, f"Property '{prop_name}' not found in "
                                   f"object '{self._operator.data_object_name}'")
            return

        # Determine if property is in grouped or ungrouped category
        found = False
        for group in self.grouped:
            # Property is in the grouped category
            for group_name, props in group.items():
                if prop_name in props:
                    index = props.index(prop_name)
                    props[index] = new_name
                    found = True
                    break
            if found:
                break

        if not found and prop_name in self.ungrouped:
            index = self.ungrouped.index(prop_name)
            self.ungrouped[index] = new_name
            found = True

    def update_property_index(
            self,
            *,
            prop_name: str,
            new_index: int
    ) -> None:
        """
        Updates the property index.

        :param prop_name: The name of the property to update.
        :param new_index: The index to set the property to.
        """

        # group = self.get_group_name(prop_name)
        # if group and prop_name in self.grouped[group]:
        #     old_index = self.grouped[group].index(prop_name)
        #
        #     # Remove form old index first, otherwise indices are off
        #     del self.grouped[group][old_index]
        #     self.grouped[group].insert(new_index, prop_name)
        # if group and prop_name in self.ungrouped:
        #     old_index = self.ungrouped.index(prop_name)
        #
        #     # Remove form old index first, otherwise indices are off
        #     del self.ungrouped[old_index]
        #     self.ungrouped.insert(new_index, prop_name)

    def verify(self, data_object: bpy.types.Object) -> None:
        """
        Verifies the group data of the provided blender object. During this
        process, the cache is automatically updated.

        :param data_object: (bpy.types.Object) The blender object that
        will be synchronized.

        :return: None
        """
        # Cleanup any unused properties from the group data
        # Retrieve properties to be removed
        data_object_keys = set(data_object.keys())
        grouped_props_to_remove = [prop
                                   for group in self.grouped
                                   for _, props in group.items()
                                   for prop in props
                                   if prop not in data_object_keys
                                   or prop.startswith("_")]
        ungrouped_props_to_remove = [prop
                                     for prop in self.ungrouped
                                     if prop not in data_object_keys
                                     or prop.startswith("_")]

        # Remove properties
        keys_to_remove = grouped_props_to_remove + ungrouped_props_to_remove
        for key in keys_to_remove:
            del self[key]

        # Add any custom properties that are in the blender object, but not
        # in the group data.
        for prop in data_object.keys():
            if prop not in self:
                self.ungrouped.append(prop)

        # Update the cache with any modified data
        GroupData._update_cache(self, data_object)

    def get_group_name(self, prop_name: str) -> str:
        for group in self.grouped:
            for group_name, props in group.items():
                if prop_name in props:
                    return group_name

        return ""

    @classmethod
    def get_data(cls, data_object: bpy.types.Object) -> Self:
        """
        INTERNAL ONLY!

        Gets the group data for the provided blender object. Data is automatically
        verified and cache is updated.

        :param data_object: The blender object to get the group data for.

        :return: The group data for the provided blender object.
        """
        # Use object's memory pointer as cache key
        object_pointer = data_object.as_pointer()

        if object_pointer in cls._cache:
            # Object is cached, get the data
            cached_data = cls._cache[object_pointer]
            new_data = GroupData(
                grouped = cached_data.get("grouped", []),
                ungrouped = cached_data.get("ungrouped", [])
            )
        else:
            new_data = GroupData()

        # Verify the newly formed CPMGroupedData
        new_data.verify(data_object)
        return new_data

    @classmethod
    def serialize(cls) -> None:
        """
        Serializes grouping data for all Blender objects. The data is
        transformed into a dictionary and then serialized as a string
        property per object.
        """
        all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
        for data_object in all_objects:
            # Store each individual object's grouping data as a
            # StringProperty on said object.
            group_data = GroupData.get_data(data_object)
            data_dict = {
                "grouped": group_data.grouped,
                "ungrouped": group_data.ungrouped
            }
            data_object[config.CPM_SERIALIZED_GROUP_DATA] = json.dumps(data_dict)

    @classmethod
    def deserialize(cls) -> None:
        """
        Deserializes grouping data for a specified object's custom properties
        using the designated private property that's already stored on the
        object as the data source.
        """

        all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
        for data_object in all_objects:
            data_str = data_object.get(config.CPM_SERIALIZED_GROUP_DATA,
                                       config.CPM_DEFAULT_GROUP_DATA)
            group_data = json.loads(data_str)
            new_data = GroupData(
                grouped = group_data.get("grouped", []),
                ungrouped = group_data.get("ungrouped", []))
            new_data.verify(data_object)

    @classmethod
    def _update_cache(cls, group_data: Self, data_object:
    bpy.types.Object) -> None:
        """
        Updates the cached group data.

        :param group_data: (PropertyGroupData) The data to use for updating.
        :param data_object: (bpy.types.Object) The Blender 
        object the data belongs to.
        """
        object_pointer = data_object.as_pointer()
        if (object_pointer not in cls._cache or
            cls._cache[object_pointer] != group_data):
            cls._cache[object_pointer] = {
                "grouped": group_data.grouped,
                "ungrouped": group_data.ungrouped
            }