import bpy, json
from typing import Dict, Self
import config


class PropertyGroupData:
    _cache = {}

    def __init__(self,
                 grouped: list[Dict[str, list[str]]] = None,
                 ungrouped: list[str] = None) -> None:
        """
        Initialize PropertyGroupData.

        :param grouped: A list of dictionaries describing groups with
        properties.
        :param ungrouped: A list of properties without groups.

        :return: None
        """
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
            for props in group.values():
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
                                   for group_name, props in group.items()
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
        PropertyGroupData._update_cache(self, data_object)

    @classmethod
    def _update_cache(cls, group_data: Self, data_object_name: str) -> None:
        """
        Updates the cached group data.

        :param group_data: (PropertyGroupData) The data to use for updating.
        :param data_object_name: (str) The name of the blender object the
        data belongs to.

        :return: None
        """
        if (data_object_name in cls._cache
                and not cls._cache[data_object_name] == group_data):
            cls._cache[data_object_name] = group_data

    @classmethod
    def get_data(cls, data_object: bpy.types.Object) -> Self:
        """
        INTERNAL ONLY!

        Gets the group data for the provided blender object. Data is automatically
        verified and cache is updated.

        :param data_object: The blender object to get the group data for.

        :return: The group data for the provided blender object.
        """
        if data_object.name in cls._cache:
            # Object is cached, get the data
            cached_data = cls._cache[data_object.name]
            new_data = PropertyGroupData(
                grouped=cached_data.get("grouped", []),
                ungrouped=cached_data.get("ungrouped", [])
            )
        else:
            new_data = PropertyGroupData()

        # Verify the newly formed CPMGroupedData
        new_data.verify(data_object)

        return new_data

    def _serialize(self, data_object: bpy.types.Object) -> None:
        """
        Serializes grouping data for a specified object's custom properties
        into a private property on the blender object.

        :param data_object: (bpy.types.Object): Object containing the properties
        to be serialized.

        :return: None
        """

        # Verify the data
        self.verify(data_object)

        # Convert to dictionary
        data_dict = {
            "grouped": self.grouped,
            "ungrouped": self.ungrouped,
        }
        data_object[config.CPM_SERIALIZED_GROUP_DATA] = json.dumps(data_dict)

    @classmethod
    def _deserialize(cls, data_object: bpy.types.Object) -> None:
        """
        Deserializes grouping data for a specified object's custom properties
        using the designated private property that's already stored on the
        object as the data source.

        :param: data_object (bpy.types.Object): Object containing properties
        to be serialized.

        :return: None
        """

        data_str = data_object.get(config.CPM_SERIALIZED_GROUP_DATA,
                                   config.CPM_DEFAULT_GROUP_DATA)
        group_data = json.loads(data_str)
        new_data = PropertyGroupData(
            grouped = group_data.get("grouped", []),
            ungrouped = group_data.get("ungrouped", [])
        )

        cls._cache[data_object.name] = new_data

        return None