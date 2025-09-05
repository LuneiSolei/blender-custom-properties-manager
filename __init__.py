from .infrastructure import AddPropertyGroupOperator, EditPropertyMenuOperator, ExpandToggleOperator, bootstrap

bl_info = {
    "name": "Custom Properties Manager",
    "author": "Lunei Solei",
    "version": (0, 0, 1),
    "blender": (4, 4, 3),
    "category": "UI",
    "location": "Properties > View Layer > Custom Properties",
    "description": "Manage custom properties"
}

_classes = {
    AddPropertyGroupOperator,
    EditPropertyMenuOperator,
    ExpandToggleOperator
}

def register():
    bootstrap.register_services()
    bootstrap.register_classes(_classes)
    bootstrap.register_draw_functions()
    bootstrap.register_handlers()

def unregister():
    bootstrap.unregister_draw_functions()
    bootstrap.clear_state()
    bootstrap.unregister_classes(_classes)
    bootstrap.unregister_handlers()

if __name__ == "__main__":
    register()