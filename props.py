import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    PointerProperty,
    CollectionProperty
)

class CPMProperty(bpy.types.PropertyGroup):
    group_name: StringProperty(name = "Unnamed Group")
    prop_name: StringProperty(name = "Unnamed Property")

class CPMPropertyGroup(bpy.types.PropertyGroup):
    """Main CPM PropertyGroup with collection of properties"""
    properties: CollectionProperty(type = CPMProperty)

class CustomPropertyProxy(bpy.types.PropertyGroup):
    """PropertyGroup that syncs with ID properties"""

    def update_id_property(self, context, prop_name):
        """Update the corresponding ID property when PropertyGroup Changes"""
        owner = self.get_owner();
        if owner and prop_name in self:
            owner[prop_name] = getattr(self, prop_name)

    def get_owner(self):
        """Find the object that owns this PropertyGroup"""

def create_synced_property(group_class, prop_name, value, update_callback =
None):
    """Create a property that syncs with ID properties"""

    def make_update_func(name):
        def update_func(self, context):
            self.update_id_property(context, name)
            if update_callback:
                update_callback(self, context)
        return update_func

    if isinstance(value, bool):
        setattr(group_class, prop_name, BoolProperty(
            default = value,
            update = make_update_func(prop_name)
        ))
    elif isinstance(value, int):
        setattr(group_class, prop_name, IntProperty(
            default = value,
            update = make_update_func(prop_name)
        ))
    elif isinstance(value, float):
        setattr(group_class, prop_name, FloatProperty(
            default=value,
            update=make_update_func(prop_name)
        ))
    elif isinstance(value, str):
        setattr(group_class, prop_name, StringProperty(
            default = value,
            update = make_update_func(prop_name)
        ))

def sync_id_properties_to_group(obj, group_name):
    # Capture existing ID properties
    id_props = {key: obj[key] for key in obj.keys()}

    # Create dynamic PropertyGroup
    class DynamicPropertyGroup(CustomPropertyProxy):
        pass

    # Add properties to group
    for prop_name, value in id_props.items():
        create_synced_property(DynamicPropertyGroup, prop_name, value)

    # Register and attach to object type
    bpy.utils.register_class(DynamicPropertyGroup)
    setattr(type(obj), group_name, PointerProperty(type=DynamicPropertyGroup))

    # Initialize values
    group = getattr(obj, group_name)
    for prop_name, value in id_props.items():
        setattr(group, prop_name, value)

    return DynamicPropertyGroup