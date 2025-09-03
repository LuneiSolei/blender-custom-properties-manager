import bpy
import json
from itertools import chain
from typing import Dict, Self
from .reporting_mixin import ReportingMixin
from ...shared import misc

class GroupData(ReportingMixin):
    _cache = {}

    def __init__(self, grouped: list[Dict[str, list[str]]] = None,
                 ungrouped: list[str] = None, *args, **kwargs):
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
        if misc.CPM_SERIALIZED_GROUP_DATA in self:
            del self[misc.CPM_SERIALIZED_GROUP_DATA]

    def __delitem__(self, prop_name):
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
                    break

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
            data_object: bpy.types.Object,
            prop_name: str,
            new_name: str
    ):
        """
        Updates name of the property.

        :param data_object: Blender data object the property belongs to.
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

        self._update_cache(self, data_object)

    def update_property_group(
            self,
            *,
            data_object: bpy.types.Object,
            prop_name: str,
            new_group: str
    ):
        """
        Updates the group the property belongs to.

        :param data_object: Blender data object the property belongs to.
        :param prop_name: The name of the property to update.
        :param new_group: The name of the group to attach the property to.
        """
        # Remove property from old group
        if not self.get_group_name(prop_name):
            self.report({'INFO'}, f"Property '{prop_name}' found in ungrouped.")
            index = self.ungrouped.index(prop_name)
            self.ungrouped.pop(index)
        else:
            for group_name, props in chain.from_iterable(group.items() for group in self.grouped):
                if prop_name in props:
                    prop_index = props.index(prop_name)
                    props.pop(prop_index)
                    break

        # Place property into the new group
        if not new_group:
            # Property goes into ungrouped category
            self.ungrouped.append(prop_name)
        else:
            self.report({'INFO'}, f"Placed property '{prop_name}' in group '{new_group}'.")
            # Property goes into grouped category
            found = False
            for group_name, props in chain.from_iterable(
                    group.items() for group in self.grouped):
                if group_name == new_group:
                    props.append(prop_name)
                    found = True
                    break

            # Group does not exist, create it
            if not found:
                self.grouped.append({new_group: [prop_name]})

        self._update_cache(self, data_object)

    def update_property_type(
            self,
            *,
            data_object: bpy.types.Object,
            prop_name: str,
            new_type: str
    ):
        """Updates the type of the property."""

    def verify(self, data_object: bpy.types.Object):
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
        for group_name, props in chain.from_iterable(
                group.items() for group in self.grouped):
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
                grouped=cached_data.get("grouped", []),
                ungrouped=cached_data.get("ungrouped", [])
            )
        else:
            new_data = GroupData()

        # Verify the newly formed GroupData
        new_data.verify(data_object)
        return new_data

    @classmethod
    def serialize(cls):
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
            data_object[misc.CPM_SERIALIZED_GROUP_DATA] = json.dumps(data_dict)

    @classmethod
    def deserialize(cls):
        """
        Deserializes grouping data for a specified object's custom properties
        using the designated private property that's already stored on the
        object as the data source.
        """

        all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
        for data_object in all_objects:
            data_str = data_object.get(misc.CPM_SERIALIZED_GROUP_DATA,
                                       misc.DEFAULT_GROUP_DATA)
            group_data = json.loads(data_str)
            new_data = GroupData(
                grouped=group_data.get("grouped", []),
                ungrouped=group_data.get("ungrouped", []))
            new_data.verify(data_object)

    @classmethod
    def _update_cache(cls, group_data: Self, data_object:
    bpy.types.Object):
        """
        Updates the cached group data.

        :param group_data: (PropertyGroupData) The data to use for updating.
        :param data_object: (bpy.types.Object) The Blender 
        object the data belongs to.
        """
        # Clean up any remaining empty groups
        group_data.grouped = [group_dict for group_dict in group_data.grouped
                              if any(len(props) > 0 for props in group_dict.values())]

        # Store the group data under the relevant data object's cache
        object_pointer = data_object.as_pointer()
        current_data = {
            "grouped": group_data.grouped,
            "ungrouped": group_data.ungrouped
        }
        if object_pointer not in cls._cache or cls._cache[object_pointer] != current_data:
            cls._cache[object_pointer] = current_data