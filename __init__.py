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



def register():
    bootstrap.setup()
    bootstrap.register_classes()
    bootstrap.register_draw_functions()
    bootstrap.register_handlers()
    bootstrap.post_setup()

def unregister():
    bootstrap.unregister_draw_functions()
    bootstrap.clear_state()
    bootstrap.unregister_classes()
    bootstrap.unregister_handlers()

if __name__ == "__main__":
    register()