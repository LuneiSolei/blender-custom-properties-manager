from .apply_handler import ApplyHandler
from ...core import Field, GroupData

class ApplyGroupHandler(ApplyHandler):
    def handle(self, field: Field, operator):
        # Check that group name has changed
        current_group = field.current_value
        new_group = operator.group
        if new_group == current_group:
            return

        # Update property group in CPM's dataset
        GroupData.get_data(operator.data_object).update_property_group(
            data_object = operator.data_object,
            prop_name = operator.name,
            new_group = new_group
        )