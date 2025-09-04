import bpy

from ...core import Field, GroupData

# noinspection PyMethodMayBeStatic
class EditPropertyService:
    # noinspection PyNoneFunctionAssignment
    def update_property_data(self, operator):
        data_object = operator.data_object

        # Check if the property type has changed
        if operator.fields["type"].current_value == operator.type:
            return

        match operator.type:
            case 'FLOAT':
                data_object[operator.name] = bpy.props.FloatProperty(
                    name = operator.name,
                    description = operator.description,
                    translation_context = operator.translation_context,
                    min = operator.min_float,
                    max = operator.max_float,
                    soft_min = operator.soft_min_float,
                    soft_max = operator.soft_max_float,
                    step = operator.step_float,
                    precision = operator.precision,
                    options = operator.options,
                    override = operator.override,
                    tags = operator.tags,
                    subtype = operator.subtype,
                    unit = operator.unit,
                    update = operator.update_callback,
                    get = operator.get,
                    set = operator.set
                )

    def update_name(self, operator, field: Field):
        """
        Updates the property name.
        :param operator: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.
        """
        # Ensure the property name has changed
        if field.current_value == operator.name:
            return

        # Validation
        if operator.name in operator.data_object:
            operator.report({'ERROR'}, f"Property '{operator.name}' already exists")

            # Reset property name
            operator.name = field.current_value

            return

        # Ensure we're not trying to rename an IDPropertyGroup
        if isinstance(operator.data_object[field.current_value], bpy.types.bpy_struct):
            operator.report({'ERROR'}, f"Cannot rename '{field.current_value}' to '"
                                       f"{operator.name}'. Renaming IDPropertyGroup "
                                       f"types is currently not supported.")

            return

        # Update property name in CPM's dataset
        group_data = GroupData.get_data(operator.data_object)
        group_data.set_operator(operator)
        group_data.update_property_name(
            data_object = operator.data_object,
            prop_name = operator.name,
            new_name = operator.name
        )

        # Update the property in the data object itself
        operator.data_object[operator.name] = operator.data_object[field.current_value]
        operator.data_object.id_properties_ui(operator.name).update(**operator.ui_data)
        del operator.data_object[field.current_value]

    def update_group(self, operator, field: Field):
        """
        Updates the property group.
        :param operator: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.
        """
        # Ensure the group name has changed
        if field.current_value == operator.group:
            return

        # Update property in CPM's dataset
        group_data = GroupData.get_data(operator.data_object)
        group_data.set_operator(operator)
        group_data.update_property_group(
            data_object = operator.data_object,
            prop_name = operator.name,
            new_group = operator.group
        )

    def _update_property(self, operator, field: Field):
        """
        Updates the property type.
        :param operator: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.
        """

        # Ensure the property type has changed
        if field.current_value == operator.type:
            return

        match operator.type:
            case 'FLOAT':
                return bpy.props.FloatProperty()

        pass