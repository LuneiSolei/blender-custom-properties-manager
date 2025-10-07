import json

from ...core import Field, FieldNames, UIData
from ...shared import consts, utils
from ...shared.utils import StructuredLogger
from ...shared.entities import LogLevel

class UIDataService:
    logger = StructuredLogger(consts.MODULE_NAME)

    @staticmethod
    def stringify_ui_data(ui_data: UIData) -> str:
        """Returns a string representation of the ui data in JSON format."""
        return json.dumps(ui_data)

    @classmethod
    def load_ui_data(cls, operator_instance) -> UIData:
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

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Loading property UI data",
            extra = {
                "data object": data_object.name,
                "property": operator_instance.name
            }
        )

        data_object = utils.resolve_data_object(operator_instance.data_path)

        # Check if property is PYTHON type (IDPropertyGroup) which has no UI data
        value = data_object[operator_instance.name]
        if type(value).__name__ == consts.PropertyTypes.ID_PROPERTY_GROUP:
            # PYTHON types have no UI data, return empty UIData
            ui_data = {}
        else:
            ui_data = data_object.id_properties_ui(operator_instance.name).as_dict()

        cls.logger.log(
            level = LogLevel.DEBUG,
            message = "Property UI data found",
            extra = {
                "ui data": {**ui_data}
            }
        )

        return UIData(**ui_data)

    @classmethod
    def update_ui_data(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper to update the property's UI data.

        :param operator_instance: The EditMenuPropertyOperator instance.
        :param fields: Dictionary of field names and values.

        :return: The updated UI data.
        """
        # PYTHON types have no UI data, return empty UIData
        if operator_instance.property_type == consts.PropertyTypes.PYTHON:
            return UIData()

        ui_data_map = {
            consts.PropertyTypes.FLOAT: lambda: cls._get_ui_data_float(operator_instance, fields),
            consts.PropertyTypes.INT: lambda: cls._get_ui_data_int(operator_instance, fields),
            consts.PropertyTypes.BOOL: lambda: cls._get_ui_data_bool(operator_instance, fields),
            consts.PropertyTypes.FLOAT_ARRAY: lambda: cls._get_ui_data_float_array(operator_instance, fields),
            consts.PropertyTypes.INT_ARRAY: lambda: cls._get_ui_data_int_array(operator_instance, fields),
            consts.PropertyTypes.BOOL_ARRAY: lambda: cls._get_ui_data_bool_array(operator_instance, fields),
            consts.PropertyTypes.STRING: lambda: cls._get_ui_data_str(operator_instance, fields)
        }

        new_ui_data = ui_data_map[operator_instance.property_type]()
        data_object = utils.resolve_data_object(operator_instance.data_path)
        data_object.id_properties_ui(operator_instance.name).update(**new_ui_data)

        return new_ui_data

    @staticmethod
    def _validate_soft_limits(operator_instance, field_map: dict[str, tuple[FieldNames, str, type]]):
        if not operator_instance.use_soft_limits:
            field_map["soft_min"] = field_map["min"]
            field_map["soft_max"] = field_map["max"]

    @classmethod
    def _get_ui_data_float(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper method to construct the property's UI data for a float.

        :param operator_instance: The EditMenuPropertyOperator instance.
        :param fields: The fields with which to construct the UI data from.

        :return: The constructed UI data.
        """
        field_map = {
            "subtype": (FieldNames.SUBTYPE, consts.DEFAULT_SUBTYPE, str),
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "min": (FieldNames.MIN, consts.DEFAULT_MIN_FLOAT, float),
            "max": (FieldNames.MAX, consts.DEFAULT_MAX_FLOAT, float),
            "soft_min": (FieldNames.SOFT_MIN, consts.DEFAULT_SOFT_MIN_FLOAT, float),
            "soft_max": (FieldNames.SOFT_MAX, consts.DEFAULT_SOFT_MAX_FLOAT, float),
            "step": (FieldNames.STEP, consts.DEFAULT_STEP_FLOAT, float),
            "precision": (FieldNames.PRECISION, consts.DEFAULT_PRECISION_FLOAT, int),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_VALUE_FLOAT, float),
        }

        cls._validate_soft_limits(operator_instance, field_map)

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _get_ui_data_float_array(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        field_map = {
            "subtype": (FieldNames.SUBTYPE_ARRAY, consts.DEFAULT_SUBTYPE, str),
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "min": (FieldNames.MIN, consts.DEFAULT_MIN_FLOAT_ARRAY, float),
            "max": (FieldNames.MAX, consts.DEFAULT_MAX_FLOAT_ARRAY, float),
            "soft_min": (FieldNames.SOFT_MIN, consts.DEFAULT_SOFT_MIN_FLOAT_ARRAY, float),
            "soft_max": (FieldNames.SOFT_MAX, consts.DEFAULT_SOFT_MAX_FLOAT_ARRAY, float),
            "step": (FieldNames.STEP, consts.DEFAULT_STEP_FLOAT_ARRAY, float),
            "precision": (FieldNames.PRECISION, consts.DEFAULT_PRECISION_FLOAT, int),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_FLOAT_ARRAY, list)
        }

        cls._validate_soft_limits(operator_instance, field_map)

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _get_ui_data_int(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper to construct UI data for an integer property.

        :param operator_instance: The EditPropertyMenu operator_instance instance.
        :param fields: The fields with which to construct UI data from.

        :return: The newly constructed UI data.
        """
        field_map = {
            "subtype": (FieldNames.SUBTYPE, consts.DEFAULT_SUBTYPE, str),
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "min": (FieldNames.MIN, consts.DEFAULT_MIN_INT, int),
            "max": (FieldNames.MAX, consts.DEFAULT_MAX_INT, int),
            "soft_min": (FieldNames.SOFT_MIN, consts.DEFAULT_SOFT_MIN_INT, int),
            "soft_max": (FieldNames.SOFT_MAX, consts.DEFAULT_SOFT_MAX_INT, int),
            "step": (FieldNames.STEP, consts.DEFAULT_STEP_INT, int),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_VALUE_INT, int),
        }

        cls._validate_soft_limits(operator_instance, field_map)

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _get_ui_data_int_array(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        field_map = {
            "subtype": (FieldNames.SUBTYPE_ARRAY, consts.DEFAULT_SUBTYPE, str),
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "min": (FieldNames.MIN, consts.DEFAULT_MIN_INT_ARRAY, int),
            "max": (FieldNames.MAX, consts.DEFAULT_MAX_INT_ARRAY, int),
            "soft_min": (FieldNames.SOFT_MIN, consts.DEFAULT_SOFT_MIN_INT_ARRAY, int),
            "soft_max": (FieldNames.SOFT_MAX, consts.DEFAULT_SOFT_MAX_INT_ARRAY, int),
            "step": (FieldNames.STEP, consts.DEFAULT_STEP_INT_ARRAY, int),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_INT_ARRAY, list)
        }

        cls._validate_soft_limits(operator_instance, field_map)

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _get_ui_data_bool(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        field_map = {
            "subtype": (FieldNames.SUBTYPE, consts.DEFAULT_SUBTYPE, str),
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_VALUE_BOOL, bool),
        }

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _get_ui_data_bool_array(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        field_map = {
            "subtype": (FieldNames.SUBTYPE, consts.DEFAULT_SUBTYPE, str),
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_BOOL_ARRAY, list)
        }

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _get_ui_data_str(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        field_map = {
            "description": (FieldNames.DESCRIPTION, consts.DEFAULT_DESCRIPTION, str),
            "default": (FieldNames.DEFAULT, consts.DEFAULT_VALUE_STRING, str),
        }

        return cls._construct_ui_data(operator_instance, fields, field_map)

    @classmethod
    def _construct_ui_data(
        cls,
        operator_instance,
        fields: dict[str, Field],
        field_map: dict[str, tuple[FieldNames, str, type]]
    ) -> UIData:
        result = {}
        for key, (field_name, default, cast_type) in field_map.items():
            attr_name = fields[field_name.value].attr_name
            value = getattr(operator_instance, attr_name, default)

            cls.logger.log(
                level=LogLevel.DEBUG,
                message="Construct UI data field value",
                extra={"key": key, "attr_name": attr_name, "value": value}
            )

            # Special handling for list type
            if cast_type is list:
                if isinstance(value, list):
                    result[key] = value
                else:
                    # Value isn't a list, use default instead
                    result[key] = default
            else:
                result[key] = cast_type(value)

        return UIData(**result)