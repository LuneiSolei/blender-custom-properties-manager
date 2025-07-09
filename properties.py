import bpy
from bpy.props import StringProperty, CollectionProperty

class CPMProperty(bpy.types.PropertyGroup):
    group_name: StringProperty(name = "Unnamed Group")
    prop_name: StringProperty(name = "Unnamed Property")

class CPMPropertyGroup(bpy.types.PropertyGroup):
    """Main CPM PropertyGroup with collection of properties"""
    properties: CollectionProperty(type = CPMProperty)