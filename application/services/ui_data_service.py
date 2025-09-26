import json

from ...core import Field, FieldNames, UIData
from ...shared import consts, utils

class UIDataService:
    @staticmethod
    def stringify_ui_data(ui_data: UIData) -> str:
        """Returns a string representation of the ui data in JSON format."""
        return json.dumps(ui_data)

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

    # BUG: I believe the property_type checker is somehow losing the property_type hint information from the constants that are used
    #  as a default value in `getattr()`. This results in a warning. Currently, the solution is to disable the
    #  PyTypeChecker.
    # noinspection PyUnboundLocalVariable
    @classmethod
    def update_ui_data(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper to update the property's UI data.

        :param operator_instance: The EditMenuPropertyOperator instance.
        :param fields: Dictionary of field names and values.

        :return: The updated UI data.
        """
        new_ui_data: UIData
        match operator_instance.property_type:
            case consts.PropertyTypes.FLOAT:
                new_ui_data = cls.construct_ui_data_float(operator_instance, fields)
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
                new_ui_data = cls.construct_ui_data_int(operator_instance, fields)
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
    def construct_ui_data_float(cls, operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper method to construct the property's UI data for a float.

        :param operator_instance: The EditMenuPropertyOperator instance.
        :param fields: The fields with which to construct the UI data from.

        :return: The constructed UI data.
        """
        field_map = {
            "min": (FieldNames.MIN, consts.DEFAULT_MIN_FLOAT, float),
            "max": (FieldNames.MAX, consts.DEFAULT_MAX_FLOAT, float),
            "soft_min": (FieldNames.SOFT_MIN, consts.DEFAULT_SOFT_MIN_FLOAT, float),
            "soft_max": (FieldNames.SOFT_MAX, consts.DEFAULT_SOFT_MAX_FLOAT, float),
            "step": (FieldNames.STEP, consts.DEFAULT_STEP_FLOAT, float),
            "precision": (FieldNames.PRECISION, consts.DEFAULT_PRECISION_FLOAT, int),
        }
        result = {
            "subtype": consts.DEFAULT_SUBTYPE,
            "description": consts.DEFAULT_DESCRIPTION,
        }

        for key, (field_name, default, cast_type) in field_map.items():
            attr_name = fields[field_name.value].attr_name
            result[key] = cast_type(getattr(operator_instance, attr_name, default))

        return UIData(**result)
        # "default": "",
        # "id_type": None,
        # "items": None


    @staticmethod
    def construct_ui_data_int(operator_instance, fields: dict[str, Field]) -> UIData:
        """
        Helper to construct UI data for an integer property.

        :param operator_instance: The EditPropertyMenu operator instance.
        :param fields: The fields with which to construct UI data from.

        :return: The newly constructed UI data.
        """
        return {
            "subtype": consts.DEFAULT_SUBTYPE,
            "description": consts.DEFAULT_DESCRIPTION,
            "min": int(getattr(operator_instance, fields[FieldNames.MIN.value].attr_name, consts.DEFAULT_MIN_INT)),
            "max": int(getattr(operator_instance, fields[FieldNames.MAX.value].attr_name, consts.DEFAULT_MAX_INT)),
            "soft_min": int(
                getattr(operator_instance, fields[FieldNames.SOFT_MIN.value].attr_name, consts.DEFAULT_SOFT_MIN_INT)),
            "soft_max": int(
                getattr(operator_instance, fields[FieldNames.SOFT_MAX.value].attr_name, consts.DEFAULT_SOFT_MAX_INT)),
            "step": int(getattr(operator_instance, "step", consts.DEFAULT_STEP_INT))
        }