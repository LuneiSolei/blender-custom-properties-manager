import bpy
import json
from ...core import GroupData
from ...shared import consts
from ...shared.utils import StructuredLogger
from ...shared.entities import LogLevel

class GroupDataManager:
    logger = StructuredLogger(consts.MODULE_NAME)
    _group_data_name: str = consts.CPM_SERIALIZED_GROUP_DATA
    _cache: dict[str, GroupData] = {}

    @classmethod
    def get_group_data(cls, data_object: bpy.types.Object) -> GroupData:
        """
        Gets the group data for the provided blender object. Data is automatically
        verified and the cache is updated.

        :param data_object: The Blender object to get the group data for.

        :return: The group data for the provided blender object.
        """
        # Use an in-memory cache of group data keyed by data_object's unique identifier
        object_id = data_object.as_pointer()

        # Return cached data if it exists
        if object_id in cls._cache:
            return cls._cache[object_id]

        # Otherwise, load from the object and cache it
        new_data = cls._load_json(data_object)
        cls._cache[object_id] = new_data

        return new_data

    @classmethod
    def _load_json(cls, data_object: bpy.types.Object) -> GroupData:
        """
        Loads the group data from a JSON string for the provided Blender object.

        :param data_object: The Blender object to get the group data for.

        :return: The group data for the provided Blender object.
        """
        data_str = data_object.get(cls._group_data_name, "{}")
        try:
            group_data = json.loads(data_str)
        except json.JSONDecodeError as e:
            cls.logger.log(
                level = LogLevel.ERROR,
                message = "Could not load group data from JSON string",
                extra = {
                    "data_str": data_str,
                    "json_decode_error": e
                }
            )

            group_data = {}

        new_data = GroupData(group_data = group_data)
        new_data.verify(data_object)

        return new_data

    @classmethod
    def on_file_save(cls):
        """
        Serializes grouping data for all Blender objects. The data is transformed into a string and stored as a custom
        property on each Blender object.
        """
        # If a cache exists, use it to update all objects
        if not hasattr(cls, "_cache"):
            all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
            for data_object in all_objects:
                group_data = cls.get_group_data(data_object)
                data_object[cls._group_data_name] = json.dumps(group_data.as_dict())

            return

        for object_id, group_data in cls._cache.items():
            # Find the corresponding data_object
            for data_object in list(bpy.data.scenes) + list(bpy.data.objects):
                if data_object.as_pointer() == object_id:
                    data_object[cls._group_data_name] = json.dumps(group_data.as_dict())

    @classmethod
    def on_file_load(cls):
        """Run after the addon is enabled. Deserializes grouping data for all Blender objects."""
        all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
        for data_object in all_objects:
            cls._load_json(data_object)