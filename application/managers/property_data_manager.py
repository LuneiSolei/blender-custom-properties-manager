import bpy

from .group_data_manager import GroupDataManager
from ..services import PropertyTypeService, UIDataService
from ...core import Field, FieldNames, UIData
from ...shared import consts, utils
from ...shared.entities import LogLevel
from ...shared.utils import StructuredLogger

class PropertyDataManager:
    property_type_service = PropertyTypeService
    ui_data_service = UIDataService
    logger = StructuredLogger(consts.MODULE_NAME)

    @staticmethod
    def load_ui_data(operator_instance) -> UIData:
        """
        Loads the UI data for the provided Blender data object.

        Example UI data for various types
            FLOAT: {
                'subtype': 'NONE',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.0,
                'soft_max': 1.0,
                'step': 0.10000000149011612,
                'precision': 3,
                'default': 1.0
            }

            FLOAT_ARRAY: {
                'subtype': 'NONE',
                'description': '',
                'min': 0.0,
                'max': 1.0,
                'soft_min': 0.29999998211860657,
                'soft_max': 1.0,
                'step': 0.10000000149011612,
                'precision': 3,
                'default': [0.3700000047683716, 0.3700000047683716, 0.3700000047683716]
            }

        :param operator_instance: The operator_instance instance. Used to determine the UI data.

        :return: An object used to manage the UI data.
        """
        data_object = utils.resolve_data_object(operator_instance.data_path)
        ui_data = data_object.id_properties_ui(operator_instance.name)

        return UIData(**ui_data.as_dict())

    @staticmethod
    def stringify_ui_data(ui_data: UIData) -> str:
        return json.dumps(ui_data)

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

        :param operator_instance: The EditPropertyMenu operator instance.
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
            "ui_data": cls._update_ui_data(operator_instance, fields),
        }

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property data updated",
            extra = {**new_data}
        )

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
            ui_data = cls.load_ui_data(operator_instance)

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

    # BUG: I believe the property_type checker is somehow losing the property_type hint information from the constants that are used
    #  as a default value in `getattr()`. This results in a warning. Currently, the solution is to disable the
    #  PyTypeChecker.
    # noinspection PyTypeChecker,PyUnboundLocalVariable
    @classmethod
    def _update_ui_data(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper to update the property's UI data.

        :param operator_instance: The EditMenuPropertyOperator instance.

        :return: The updated UI data.
        """
        new_ui_data: UIData
        match operator_instance.property_type:
            case consts.PropertyTypes.FLOAT:
                new_ui_data = {
                    "subtype": consts.DEFAULT_SUBTYPE,
                    "description": consts.DEFAULT_DESCRIPTION,
                    "min": getattr(operator_instance, fields[FieldNames.MIN.value].attr_name, consts.DEFAULT_MIN_FLOAT),
                    "max": getattr(operator_instance, fields[FieldNames.MAX.value].attr_name, consts.DEFAULT_MAX_FLOAT),
                    "soft_min": getattr(operator_instance, fields[FieldNames.SOFT_MIN.value].attr_name, consts.DEFAULT_SOFT_MIN_FLOAT),
                    "soft_max": getattr(operator_instance, fields[FieldNames.SOFT_MAX.value].attr_name, consts.DEFAULT_SOFT_MAX_FLOAT),
                    "step": getattr(operator_instance, "step", consts.DEFAULT_STEP_FLOAT),
                    "precision": getattr(operator_instance, "precision", consts.DEFAULT_PRECISION_FLOAT),
                    # "default": "",
                    # "id_type": None,
                    # "items": None
                }
            case consts.PropertyTypes.FLOAT_ARRAY:
                new_ui_data = {
                    "subtype": consts.DEFAULT_SUBTYPE,
                    "description": consts.DEFAULT_DESCRIPTION,
                    "min": int(getattr(operator_instance, fields[FieldNames.MIN.value].attr_name, consts.DEFAULT_MIN_FLOAT_ARRAY)),
                    "max": getattr(operator_instance, fields[FieldNames.MAX.value].attr_name, consts.DEFAULT_MAX_FLOAT_ARRAY),
                    "soft_min": getattr(operator_instance, fields[FieldNames.SOFT_MIN.value].attr_name, consts.DEFAULT_SOFT_MIN_FLOAT_ARRAY),
                    "soft_max": getattr(operator_instance, fields[FieldNames.SOFT_MAX.value].attr_name, consts.DEFAULT_SOFT_MAX_FLOAT_ARRAY),
                    "step": getattr(operator_instance, "step", consts.DEFAULT_STEP_FLOAT_ARRAY),
                    "precision": getattr(operator_instance, "precision", consts.DEFAULT_PRECISION_FLOAT_ARRAY),
                    "default": getattr(operator_instance, "default", consts.DEFAULT_VALUE_FLOAT_ARRAY)
                }
            case consts.PropertyTypes.INT:
                new_ui_data = cls._construct_ui_data_int(operator_instance, fields)
            case consts.PropertyTypes.INT_ARRAY:
                new_ui_data = {
                    "subtype": consts.DEFAULT_SUBTYPE,
                    "description": consts.DEFAULT_DESCRIPTION,
                    "min": getattr(operator_instance, fields[FieldNames.MIN.value].attr_name, consts.DEFAULT_MIN_INT_ARRAY),
                    "max": getattr(operator_instance, fields[FieldNames.MAX.value].attr_name, consts.DEFAULT_MAX_INT_ARRAY),
                    "soft_min": getattr(operator_instance, fields[FieldNames.SOFT_MIN.value].attr_name, consts.DEFAULT_SOFT_MIN_INT_ARRAY),
                    "soft_max": getattr(operator_instance, fields[FieldNames.SOFT_MAX.value].attr_name, consts.DEFAULT_SOFT_MAX_INT_ARRAY),
                    "step": getattr(operator_instance, "step", consts.DEFAULT_STEP_INT_ARRAY),
                    "default": getattr(operator_instance, "default", consts.DEFAULT_VALUE_INT_ARRAY)
                }
            case consts.PropertyTypes.BOOL:
                new_ui_data = {
                    "subtype": consts.DEFAULT_SUBTYPE,
                    "description": consts.DEFAULT_DESCRIPTION
                }
            case consts.PropertyTypes.BOOL_ARRAY:
                new_ui_data = {
                    "subtype": consts.DEFAULT_SUBTYPE,
                    "description": consts.DEFAULT_DESCRIPTION,
                    "default": consts.DEFAULT_VALUE_BOOL_ARRAY
                }
            case consts.PropertyTypes.STRING:
                new_ui_data = {

                }

        data_object = utils.resolve_data_object(operator_instance.data_path)
        data_object.id_properties_ui(operator_instance.name).update(**new_ui_data)

    @classmethod
    def _construct_ui_data_int(cls, operator, fields: dict[str, Field]) -> dict:
        """
        Helper to construct UI data for an integer property.

        :param operator: The EditPropertyMenu operator instance.
        :param fields: The fields with which to construct UI data from.

        :return: The newly constructed UI data.
        """

        return {
            "subtype": consts.DEFAULT_SUBTYPE,
            "description": consts.DEFAULT_DESCRIPTION,
            "min": int(getattr(operator, fields[FieldNames.MIN.value].attr_name, consts.DEFAULT_MIN_INT)),
            "max": int(getattr(operator, fields[FieldNames.MAX.value].attr_name, consts.DEFAULT_MAX_INT)),
            "soft_min": int(
                getattr(operator, fields[FieldNames.SOFT_MIN.value].attr_name, consts.DEFAULT_SOFT_MIN_INT)),
            "soft_max": int(
                getattr(operator, fields[FieldNames.SOFT_MAX.value].attr_name, consts.DEFAULT_SOFT_MAX_INT)),
            "step": int(getattr(operator, "step", consts.DEFAULT_STEP_INT))
        }