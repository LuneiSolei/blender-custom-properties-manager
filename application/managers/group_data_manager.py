import bpy, json
from json import JSONDecodeError
from ...core import GroupData
from ...shared import consts

class GroupDataManager:
    _group_data_name: str = consts.CPM_SERIALIZED_GROUP_DATA

    @classmethod
    def get_data(cls, data_object: bpy.types.Object) -> GroupData:
        """
        Gets the group data for the provided blender object. Data is automatically
        verified and the cache is updated.
        :param data_object: The Blender object to get the group data for.
        :return: The group data for the provided blender object.
        """

        new_data = cls._load_json(data_object)

        return new_data

    @classmethod
    def _load_json(cls, data_object: bpy.types.Object) -> GroupData:
        data_str = data_object.get(cls._group_data_name, "{}")
        try:
            group_data = json.loads(data_str)
        except JSONDecodeError as e:
            print(e)
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
        all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
        for data_object in all_objects:
            group_data = GroupDataManager.get_data(data_object)
            data_object[cls._group_data_name] = json.dumps(group_data.as_dict())

    @classmethod
    def on_file_load(cls):
        """
        Run after the addon is enabled. Deserializes grouping data for all Blender objects.
        """

        all_objects = list(bpy.data.scenes) + list(bpy.data.objects)
        for data_object in all_objects:
            cls._load_json(data_object)