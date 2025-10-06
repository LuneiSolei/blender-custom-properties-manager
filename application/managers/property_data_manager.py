from typing import Union

import bpy

from .group_data_manager import GroupDataManager
from ..services import PropertyTypeService, UIDataService
from ...core import Field, FieldNames
from ...shared import consts, utils
from ...shared.entities import LogLevel
from ...shared.utils import StructuredLogger

class PropertyDataManager:
    property_type_service = PropertyTypeService
    ui_data_service = UIDataService
    logger = StructuredLogger(consts.MODULE_NAME)

    @classmethod
    def get_array_length(cls, operator_instance) -> int:
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Getting array length",
            extra = {}
        )

        if (cls.property_type_service.get_type(operator_instance) in (
            consts.PropertyTypes.FLOAT_ARRAY,
            consts.PropertyTypes.INT_ARRAY,
            consts.PropertyTypes.BOOL_ARRAY
        )):
            return len(operator_instance.value)

        return 0

    @classmethod
    def validate(cls, data_path: str, property_name: str) -> bool:
        """
        Validate a property's existence from a data path.

        :param data_path: Path to the Blender object.
        :param property_name: Name of the property to validate.

        :return: The data object if the property exists, None otherwise.
        """
        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Validating property",
            extra = {
                "data_path": data_path,
                "property_name": property_name,
            }
        )

        # Get the data object
        data_object = utils.resolve_data_object(data_path)
        if not data_object:
            cls.logger.log(
                level = LogLevel.ERROR,
                message = "Could not find data object from data path",
                extra = {
                    "data_path": data_path
                }
            )

            return False

        # Get the property
        if property_name not in data_object:
            cls.logger.log(
                level = LogLevel.ERROR,
                message = "Could not find property from data object",
                extra = {
                    "data_object": data_object.name,
                    "property": property_name
                }
            )

            return False

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property is valid"
        )

        return True

    @classmethod
    def update_property_data(cls, operator_instance):
        """
        Update the property data for the provided Blender data object.

        :param operator_instance: The EditPropertyMenu operator_instance instance.
        """
        fields = operator_instance.field_manager.load_fields(operator_instance.fields)

        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Updating property data",
            extra = {
                "property": fields[FieldNames.NAME.value].current_value
            }
        )

        new_data = {
            "name": cls._update_name(operator_instance, fields[FieldNames.NAME.value]),
            "group": cls._update_group(operator_instance, fields[FieldNames.GROUP.value]),
            "type": cls.property_type_service.update_type(operator_instance, fields[FieldNames.TYPE.value]),
            "ui_data": cls.ui_data_service.update_ui_data(operator_instance, fields),
            "overridable_library": cls._update_overridable_library(operator_instance,
                                                                   fields[FieldNames.IS_OVERRIDABLE_LIBRARY.value])
        }

        if operator_instance.property_type in [
            consts.PropertyTypes.FLOAT_ARRAY,
            consts.PropertyTypes.INT_ARRAY,
            consts.PropertyTypes.BOOL_ARRAY
        ]:
            # noinspection PyTypeChecker
            new_data["array_length"] = cls._update_array_length(operator_instance)

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property data updated",
            extra = {**new_data}
        )

    @classmethod
    def _update_array_length(cls, operator_instance) -> Union[None, int]:
        """Resize the array when length changes"""
        if not getattr(operator_instance, "initialized", False):
            return None

        data_object = utils.resolve_data_object(operator_instance.data_path)
        new_length = operator_instance.array_length
        current_value = data_object[operator_instance.name]
        current_length = len(current_value)

        if new_length == current_length:
            return current_length # No change needed

        # Truncate or pad with defaults
        if new_length > current_length:
            pad_value = current_value[-1] if current_length > 0 else 0
            new_value = list(current_value) + [pad_value] * (new_length - current_length)
        else:
            new_value = list(current_value[:new_length])

        # Get UI data to preserve it
        ui_data = cls.ui_data_service.load_ui_data(operator_instance)

        # Delete and recreate since IDPropertyArray is a fixed size
        del data_object[operator_instance.name]
        data_object[operator_instance.name] = new_value

        # Restore UI data
        prop_instance = data_object.id_properties_ui(operator_instance.name)
        prop_instance.update(**ui_data)

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Array length updated",
            extra = {"current_length": current_length, "new_length": new_length}
        )

        return new_length

    @classmethod
    def _update_name(cls, operator_instance, field: Field) -> str:
        """
        Helper to update the property's name.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.

        :return: The new name of the property.
        """
        def has_name_changed() -> bool:
            """
            Check if the property name has changed.

            :return: True if the property name has changed, False otherwise.
            """
            return old_name != new_name

        def is_name_valid() -> bool:
            """
            Check if the property name is valid.

            :return: True if the property name is valid, False otherwise.
            """
            if operator_instance.name in data_object:
                cls.logger.log(
                    level = LogLevel.DEBUG,
                    message = "Property name already exists in data object",
                    extra = {
                        "data_object": data_object.name,
                        "property": new_name
                    }
                )

                # Reset property name
                operator_instance.name = old_name

                return False

            return True

        def is_not_id_property_group() -> bool:
            """
            Check if the property is not an ID Property Group.

            :return: True if the property is an ID Property Group, False otherwise.
            """
            if isinstance(data_object[field.current_value], bpy.types.bpy_struct):
                # Property is of IDPropertyGroup type
                cls.logger.log(
                    level = LogLevel.ERROR,
                    message = "Renaming ID Property Group types is currently not supported",
                    extra = {
                        "property": old_name
                    }
                )

                return False

            return True

        def update_data_object_prop_name():
            """Update the property's name in the data object."""
            cls.logger.log(
                level = LogLevel.DEBUG,
                message = "Updating property name in data object",
                extra = {
                    "old_name": old_name,
                    "new_name": new_name,
                    "data_object": data_object.name
                }
            )

            # Temporarily set the old name to load UI data
            operator_instance.name = old_name
            ui_data = cls.ui_data_service.load_ui_data(operator_instance)

            # Restore the new name
            operator_instance.name = new_name

            # Update the UI Data for the new property
            cls.logger.log(
                level = LogLevel.DEBUG,
                message = "Transferring UI data to new property",
                extra = {
                    "ui_data": ui_data
                }
            )

            data_object[new_name] = data_object[old_name]
            data_object.id_properties_ui(new_name).update(**ui_data)
            del data_object[old_name]

        # Log method entry
        old_name = field.current_value
        new_name = operator_instance.name
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Updating property name",
            extra = {
                "old_name": old_name,
                "new_name": new_name
            }
        )

        data_object = utils.resolve_data_object(operator_instance.data_path)
        name_change_validity = {
            "has_name_changed": has_name_changed(),
            "is_name_valid": is_name_valid(),
            "is_not_id_property_group": is_not_id_property_group(),
        }

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Finished checking validity of property name",
            extra = {
                "old_name": old_name,
                "new_name": new_name,
                "results": {**name_change_validity}
            }
        )

        # Ensure the name has changed, is valid, and is not an ID Property Group
        if not all(name_change_validity.values()):
            # Property rename not needed
            return old_name

        # Update the property name in the group data
        group_data = GroupDataManager.get_group_data(data_object)
        group_data.update_property_name(
            data_object = data_object,
            prop_name = old_name,
            new_name = new_name
        )

        # Update the property name in the data object
        update_data_object_prop_name()

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Finished updating property name",
            extra = {
                "old_name": old_name,
                "new_name": new_name,
            }
        )

        return new_name

    @classmethod
    def _update_group(cls, operator_instance, field: Field) -> str:
        """
        Helper to update the property's group.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.

        :return: The updated group name.
        """
        old_group = field.current_value
        new_group = operator_instance.group

        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Updating property's group",
            extra = {
                "old_group": old_group,
                "new_group": new_group,
            }
        )

        # Ensure the group name has changed
        if old_group == new_group:
            # Group change not needed
            return old_group

        # Update property in CPM's dataset
        data_object = utils.resolve_data_object(operator_instance.data_path)
        group_data = GroupDataManager.get_group_data(data_object)
        group_data.set_operator(operator_instance)
        group_data.update_property_group(
            prop_name = operator_instance.name,
            new_group = operator_instance.group
        )

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Updated property's group",
            extra = {
                "old_group": old_group,
                "new_group": new_group,
            }
        )

        return new_group

    @classmethod
    def _update_overridable_library(cls, operator_instance, field: Field) -> bool:
        data_object = utils.resolve_data_object(operator_instance.data_path)
        prop_name = operator_instance.name
        is_overridable = operator_instance.is_property_overridable_library
        result = data_object.property_overridable_library_set(f'["{prop_name}"]', is_overridable)

        return is_overridable if result else False