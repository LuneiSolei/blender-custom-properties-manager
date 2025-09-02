from collections import namedtuple

Panel = namedtuple("Panel", ["name", "data_path"])
panels = [
    Panel("VIEWLAYER_PT_layer_custom_props", "view_layer"),
    Panel("SCENE_PT_custom_props", "scene"),
    Panel("OBJECT_PT_custom_props", "active_object"),
    Panel("DATA_PT_custom_props_light", "active_object.data"),
]