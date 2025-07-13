import json, bpy
from . import config
from .CPMGroupData import CPMGroupData

# Global storage for expand/collapse states
expand_states = {}
_cache = {}

def serialize_cpm_groups(data_object: bpy.types.Object,
                         group_data: CPMGroupData) -> None:
    """
    Serializes grouping data for a specified object's custom properties.
    Args:
        :param data_object: (bpy.types.Object): Object containing the properties
            to be serialized.
        :param group_data: (CPMGroupData): Group data to be serialized.
    """

    # Convert to dictionary
    data_dict = {
        "grouped": group_data.grouped,
        "ungrouped": group_data.ungrouped,
    }
    data_object[config.CPM_SERIALIZED_GROUP_DATA] = json.dumps(data_dict)

    # Data has changed, clear the cache for the data_object
    _clear_cache(data_object)

def deserialize_object_cpm_group_data(data_object: bpy.types.Object) -> CPMGroupData:
    """
    Load grouping data for a specified object's custom properties
    Args:
        :param: data_object (bpy.types.Object): Object containing properties to be serialized.
    """

    # Check for cached data first
    if data_object.name in _cache:
        return _cache[data_object.name]

    # No cached data, so deserialize and store value in cache
    data_str = data_object.get(config.CPM_SERIALIZED_GROUP_DATA, config.CPM_DEFAULT_GROUP_DATA)
    group_data = json.loads(data_str)
    cpm_group_data = CPMGroupData(
        grouped=group_data.get("grouped", []),
        ungrouped=group_data.get("ungrouped", []),
    )

    _cache[data_object.name] = cpm_group_data

    return cpm_group_data

def _clear_cache(data_object):
    """Clear cache for specific object or all objects"""
    if data_object:
        _cache.pop(data_object.name, None)
    else:
        _cache.clear()