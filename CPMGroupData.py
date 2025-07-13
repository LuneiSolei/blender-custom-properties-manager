import bpy
from typing import Dict

class CPMGroupData:
    def __init__(self,
                 grouped: list[Dict[str, list[str]]] = None,
                 ungrouped: list[str] = None):
        self.grouped = grouped if grouped is not None else []
        self.ungrouped = ungrouped if ungrouped is not None else []

    def __delitem__(self, key):
        if key in self.ungrouped:
            self.ungrouped.remove(key)

        for group in self.grouped:
            for props in group.values():
                if key in props:
                    props.remove(key)

    def __contains__(self, key: str) -> bool:
        # Check ungrouped data first
        if key in self.ungrouped:
            return True

        return any(key in props
                   for group in self.grouped
                   for props in group.values())

    def cleanup(self, data_object: bpy.types.Object):
        # For each group in "grouped", get each group of properties.
        # For each property in that properties list, if said property is not in
        # data_object's keys, add it to grouped_props_to_remove.
        data_object_keys = set(data_object.keys())
        grouped_props_to_remove = [prop
                                   for group in self.grouped
                                   for group_name, props in group.items()
                                   for prop in props
                                   if prop not in data_object_keys]

        # For each property in the "ungrouped" properties list, if said property
        # is not in data_object's keys, add it to ungrouped_props_to_remove.
        ungrouped_props_to_remove = [prop
                                     for prop in self.ungrouped
                                     if prop not in data_object_keys]

        # Remove properties
        keys_to_remove = grouped_props_to_remove + ungrouped_props_to_remove
        for key in keys_to_remove:
            del self[key]

    def update(self, data_object: bpy.types.Object):
        """Checks data_object for properties not found in group data and
        appends them to \"ungrouped\""""
        for prop in data_object.keys():
            if prop not in self:
                self.ungrouped.append(prop)