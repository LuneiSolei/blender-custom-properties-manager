import logging

PROPERTY_TYPES = (
    ('FLOAT', "Float", "A single floating-point value"),
    ('FLOAT_ARRAY', "Float Array", "An array of floating-point values"),
    ('INT', "Integer", "A single integer"),
    ('INT_ARRAY', "Integer Array", "An array of integers"),
    ('BOOL', "Boolean", "A true or false value"),
    ('BOOL_ARRAY', "Boolean Array", "An array of true or false values"),
    ('STRING', "String", "A string value"),
    ('DATA_BLOCK', "Data-Block", "A data-block value"),
    ('PYTHON', "Python", "Edit a Python value directly, for unsupported property types"),
)  # https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L138

class PropertyTypes:
    FLOAT = PROPERTY_TYPES[0][0]
    FLOAT_ARRAY = PROPERTY_TYPES[1][0]
    INT = PROPERTY_TYPES[2][0]
    INT_ARRAY = PROPERTY_TYPES[3][0]
    BOOL = PROPERTY_TYPES[4][0]
    BOOL_ARRAY = PROPERTY_TYPES[5][0]
    STRING = PROPERTY_TYPES[6][0]
    DATA_BLOCK = PROPERTY_TYPES[7][0]
    PYTHON = PROPERTY_TYPES[8][0]
    ID_PROPERTY_ARRAY = "IDPropertyArray"

PROPERTY_SUBTYPES = (
    ('NONE', "Plain Data", "Data values without special behavior"),
    ('PIXEL', "Pixel", "A distance on screen"),
    ('PERCENTAGE', "Percentage", "A percentage between 0 and 100"),
    ('FACTOR', "Factor", "A factor between 0.0 and 1.0"),
    ('ANGLE', "Angle", "A rotational value specified in radians"),
    ('TIME_ABSOLUTE', "Time", "Time specified in seconds"),
    ('DISTANCE', "Distance", "A distance between two points"),
    ('POWER', "Power", ""),
    ('TEMPERATURE', "Temperature", "")
)  # https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1397

PROPERTY_SUBTYPE_VECTORS = (
    ('NONE', "Plain Data", "Data values without special behavior"),
    ('COLOR', "Linear Color", "Color in the linear space"),
    ('COLOR_GAMMA', "Gamma-Corrected Color", "Color in the gamma corrected space"),
    ('TRANSLATION', "Translation", ""),
    ('DIRECTION', "Direction", ""),
    ('VELOCITY', "Velocity", ""),
    ('ACCELERATION', "Acceleration", ""),
    ('EULER', "Euler Angles", "Euler rotation angles in radians"),
    ('QUATERNION', "Quaternion Rotation", "Quaternion rotation (affects NLA blending)"),
    ('AXISANGLE', "Axis-Angle", "Angle and axis to rotate around"),
    ('XYZ', "XYZ", "")
)  # https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1409

LOG_LEVELS = (
    (str(logging.CRITICAL + 1), "None", "Shows no messages"),
    (str(logging.DEBUG), "Debug", "Shows debug, info, warning, error, and critical messages"),
    (str(logging.INFO), "Info", "Shows info, warning, error, and critical messages"),
    (str(logging.WARNING), "Warning", "Shows warning error, and critical messages"),
    (str(logging.ERROR), "Error", "Shows error and critical messages"),
    (str(logging.CRITICAL), "Critical", "Shows only critical messages"),
)

