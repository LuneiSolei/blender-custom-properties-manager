import bpy, json

from ...core import Field, FieldNames, UIData
from .group_data_manager import GroupDataManager
from ...shared import consts, utils
from ...shared.utils import StructuredLogger
from ...shared.entities import LogLevel

class PropertyDataManager:
    TYPE_MAP = {
        "float": consts.PropertyTypes.FLOAT,
        "float_array": consts.PropertyTypes.FLOAT_ARRAY,
        "int": consts.PropertyTypes.INT,
        "int_array": consts.PropertyTypes.INT_ARRAY,
        "bool": consts.PropertyTypes.BOOL,
        "bool_array": consts.PropertyTypes.BOOL_ARRAY,
        "string": consts.PropertyTypes.STRING,
        "IDPropertyGroup": consts.PropertyTypes.PYTHON,
        "data_block": consts.PropertyTypes.DATA_BLOCK
    }

    logger = StructuredLogger(consts.MODULE_NAME)

    @classmethod
    def get_type(cls, operator_instance) -> str:
        """
        Get the property's type from the operator_instance instance.

        :param operator_instance: The EditPropertyMenuOperator instance.

        :return: One of the PropertyTypes enum values
        """
        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Getting property type",
            extra = {
                "data_path": operator_instance.data_path,
                "prop_name": operator_instance.name,
            }
        )

        # Initialize property data
        data_object = utils.resolve_data_object(operator_instance.data_path)
        prop_name = operator_instance.name
        value = data_object[prop_name]
        prop_type = type(value).__name__
        return_value: str

        # Check if it's a standard property_type
        if prop_type in PropertyDataManager.TYPE_MAP:
            return_value = PropertyDataManager.TYPE_MAP[prop_type]

        # Check if it's an array property_type
        elif prop_type == consts.PropertyTypes.ID_PROPERTY_ARRAY:
            return_value = PropertyDataManager._determine_array_type(value)

        # Check if it's a data block property_type
        elif isinstance(value, bpy.types.ID):
            return_value = consts.PropertyTypes.DATA_BLOCK

        # Default fallback
        else:
            cls.logger.log(
                level = LogLevel.ERROR,
                message = "Property type not supported",
                extra = {
                    "property_type": prop_type
                }
            )

            return consts.PropertyTypes.FLOAT

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property type found",
            extra = {
                "property_type": prop_type,
            }
        )

        return return_value

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
            "type": cls._update_type(operator_instance, fields[FieldNames.TYPE.value]),
            "ui_data": cls._update_ui_data(operator_instance, fields),
        }

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property data updated",
            extra = {**new_data}
        )

    # noinspection PyUnboundLocalVariable
    @classmethod
    def _determine_array_type(cls, value: list) -> consts.PropertyTypes:
        """
        Helper to determine the array property_type.

        :param value: The value of the array.

        :return: One of the PropertyTypes enum values.
        """
        # Log method entry
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Determining array property type",
            extra = {
                "value": value
            }
        )

        return_value: consts.PropertyTypes
        if not value:
            # A value was not provided
            cls.logger.log(
                level = LogLevel.WARNING,
                message = "No value provided to determine array property type"
            )
            return consts.PropertyTypes.FLOAT_ARRAY

        match value[0]:
            case float():
                return_value = consts.PropertyTypes.FLOAT_ARRAY
            case int():
                return_value = consts.PropertyTypes.INT_ARRAY
            case bool():
                return_value = consts.PropertyTypes.BOOL_ARRAY
            case _:
                # We have an incorrect property type
                cls.logger.log(
                    level = LogLevel.ERROR,
                    message = "Array property type must be of float, int, or bool",
                    extra = {
                        "value": value[0],
                        "type": type(value[0])
                    }
                )
                return_value = consts.PropertyTypes.FLOAT_ARRAY

        # Log method exit
        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Array property type found",
            extra = {
                "type": return_value
            }
        )

        return return_value

    @classmethod
    def _update_name(cls, operator_instance, field: Field):
        """
        Helper to update the property's name.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.
        """
        def has_name_changed() -> bool:
            """
            Check if the property name has changed.

            :return: True if the property name has changed, False otherwise.
            """
            return field.current_value != operator_instance.name

        def is_name_valid() -> bool:
            """
            Check if the property name is valid.

            :return: True if the property name is valid, False otherwise.
            """
            if operator_instance.name in data_object:
                utils.log(
                    message = f"Property name '{operator_instance.name}' already exists in the data object.",
                    level = LogLevel.DEBUG
                )

                # Reset property name
                operator_instance.name = field.current_value

                return False

            return True

        def is_not_id_property_group() -> bool:
            """
            Check if the property is not an ID Property Group.

            :return: True if the property is an ID Property Group, False otherwise.
            """
            if isinstance(data_object[field.current_value], bpy.types.bpy_struct):
                utils.log(
                    level = LogLevel.ERROR,
                    message = f"Cannot rename property '{field.current_value}' to '{field.name}'. Renaming"
                              f"IDPropertyGroup types is currently not supported."
                )

                return False

            return True

        def update_group_data():
            """Update the property's group data in the CPM dataset."""
            group_data = GroupDataManager.get_group_data(data_object)
            group_data.update_property_name(
                data_object=data_object,
                prop_name=field.current_value,
                new_name=operator_instance.name
            )

        def update_data_object_prop_name():
            """Update the property's name in the data object."""
            utils.log(
                level = LogLevel.DEBUG,
                message = f"Updating property name in data object '{data_object.name}'"
            )

            # Temporarily store the new name
            new_name = operator_instance.name

            # Temporarily set the old name to load UI data
            operator_instance.name = field.current_value
            ui_data = cls.load_ui_data(operator_instance)

            # Restore the new name
            operator_instance.name = new_name

            # Update the UI Data for the new property
            utils.log(
                level = LogLevel.DEBUG,
                message = f"Updating UI info.\n"
                          f"UI Info: {ui_data}"
            )

            data_object[operator_instance.name] = data_object[field.current_value]
            data_object.id_properties_ui(operator_instance.name).update(**ui_data)
            del data_object[field.current_value]

            utils.log(
                level = LogLevel.DEBUG,
                message = f"Property name in data object update successful."
            )

        data_object = utils.resolve_data_object(operator_instance.data_path)

        name_change_validity = {
            "has_name_changed": has_name_changed(),
            "is_name_valid": is_name_valid(),
            "is_not_id_property_group": is_not_id_property_group(),
        }

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Renaming property '{field.current_value}...'"
        )

        utils.log(
            level = LogLevel.DEBUG,
            message = f"{name_change_validity}"
        )

        # Ensure the name has changed, is valid, and is not an ID Property Group
        if not all(name_change_validity.values()):
            utils.log(
                level = LogLevel.DEBUG,
                message = f"Property rename not needed. Cancelling..."
            )
            return

        update_group_data()
        update_data_object_prop_name()
        utils.log(
            level = LogLevel.DEBUG,
            message = f"Property renamed from '{field.current_value}' to '{operator_instance.name}'"
        )

    @staticmethod
    def _update_group(operator_instance, field: Field):
        """
        Helper to update the property's group.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param field: The field with the data used to update the property.
        """
        # Ensure the group name has changed
        if field.current_value == operator_instance.group:
            return

        # Update property in CPM's dataset
        data_object = utils.resolve_data_object(operator_instance.data_path)
        group_data = GroupDataManager.get_group_data(data_object)
        group_data.set_operator(operator_instance)
        group_data.update_property_group(
            prop_name = operator_instance.name,
            new_group = operator_instance.group
        )

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Property '{operator_instance.name}' moved to group '{operator_instance.group}'"
        )

    @staticmethod
    def _update_type(operator_instance, field: Field):
        """
        Helper to update the property's property_type.

        :param operator_instance: The EditMenuPropertyOperator instance.
        :param field: The field with the data used to update the property.
        """

        # Get the current property type from the data object to compare
        current_property_type = PropertyDataManager.get_type(operator_instance)

        if operator_instance.property_type == current_property_type:
            return

        new_value = None
        match operator_instance.property_type:
            case consts.PropertyTypes.FLOAT:
                new_value = float(field.current_value) if isinstance(field.current_value, (int, float)) else 0.0
            case consts.PropertyTypes.INT:
                new_value = int(field.current_value) if isinstance(field.current_value, (int, float)) else 0
            case consts.PropertyTypes.BOOL:
                new_value = bool(field.current_value)
            case consts.PropertyTypes.STRING:
                new_value = str(field.current_value)
            case consts.PropertyTypes.FLOAT_ARRAY:
                if isinstance(field.current_value, list):
                    new_value = [float(v) if isinstance(v, (int, float)) else 0.0 for v in field.current_value]
                else:
                    new_value = [float(field.current_value) if isinstance(field.current_value, (int, float)) else 0.0]
            case consts.PropertyTypes.INT_ARRAY:
                if isinstance(field.current_value, list):
                    new_value = [int(v) if isinstance(v, (int, float)) else 0 for v in field.current_value]
                else:
                    new_value = [int(field.current_value) if isinstance(field.current_value, (int, float)) else 0]
            case consts.PropertyTypes.BOOL_ARRAY:
                if isinstance(field.current_value, list):
                    new_value = [bool(v) for v in field.current_value]
                else:
                    new_value = [bool(field.current_value)]
            case consts.PropertyTypes.PYTHON:
                new_value = {} if not isinstance(field.current_value, dict) else field.current_value

        utils.log(
            level = LogLevel.DEBUG,
            message = f"New Property Type: {new_value}"
        )

        # Update the property with the new value as the new property_type
        data_object = utils.resolve_data_object(operator_instance.data_path)
        data_object[operator_instance.name] = new_value

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Property '{operator_instance.name}' type changed from {current_property_type} to {operator_instance.property_type}"
        )

    # BUG: I believe the property_type checker is somehow losing the property_type hint information from the constants that are used
    #  as a default value in `getattr()`. This results in a warning. Currently, the solution is to disable the
    #  PyTypeChecker.
    # noinspection PyTypeChecker,PyUnboundLocalVariable
    @classmethod
    def _update_ui_data(cls, operator_instance, fields: dict[str, Field]):
        """
        Helper to update the property's UI data.

        :param operator_instance: The EditMenuPropertyOperator instance.
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

        utils.log(
            level = LogLevel.DEBUG,
            message = f"New UI Data: {new_ui_data}"
        )

        data_object = utils.resolve_data_object(operator_instance.data_path)
        data_object.id_properties_ui(operator_instance.name).update(**new_ui_data)

    @staticmethod
    def _construct_ui_data_int(operator, fields: dict[str, Field]) -> dict:
        """
        Helper to construct UI data for an integer property.

        :param operator: The EditPropertyMenu operator instance.
        :param fields: The fields with which to construct UI data from.

        :return: The newly constructed UI data.
        """

        ui_data = {
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

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Int UI Data: {ui_data}"
        )


        return ui_data

    @staticmethod
    def on_type_change(operator_instance, context):
        """
        Called when the property property_type changes.

        :param operator_instance: The EditPropertyMenuOperator instance.
        :param context: The Blender context.
        """

        # Prevent infinite recursion
        if not getattr(operator_instance, "initialized", False):
            return

        utils.log(
            level = LogLevel.DEBUG,
            message = f"Property type changed to {operator_instance.property_type}, refreshing fields"
        )

        operator_type = utils.get_blender_operator_type(consts.CPM_EDIT_PROPERTY)
        operator_instance.fields = operator_type.field_manager.setup_fields(operator_instance, operator_type)
