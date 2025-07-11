import json, bpy
from typing import Dict
from . import config

# Global storage for expand/collapse states
expand_states = {}
cpm_groups = {}

def serialize_cpm_groups(data_object: bpy.types.Object,
                         cpm_group_data: Dict[str, list[str | Dict[str, str]]]):
    """
    Serializes grouping data for a specified object's custom properties.
    Args:
        :param data_object: (bpy.types.Object): Object containing the properties
            to be serialized.
        :param cpm_group_data: (Dict[str, list[str | Dict[str, str]]]): Group
            data of the object's custom properties.
    """

    if "grouped" and "ungrouped" in cpm_group_data:
        data_object[config.CPM_SERIALIZED_GROUP_DATA] = json.dumps(cpm_group_data)

def deserialize_object_cpm_group_data(data_object: bpy.types.Object) -> (
        Dict)[str, list[str | Dict[str, str]]]:
    """
    Load grouping data for a specified object's custom properties
    Args:
        :param: data_object (bpy.types.Object): Object containing properties to be serialized.
    """

    data_str = data_object.get(config.CPM_SERIALIZED_GROUP_DATA, config.CPM_DEFAULT_GROUP_DATA)
    return json.loads(data_str)