CUSTOM_PROPERTY_TYPE_ITEMS = (
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

PROPERTY_SUBTYPE_ITEMS = (
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

PROPERTY_SUBTYPE_VECTOR_ITEMS = (
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