def on_min_max_float_update(operator, _context):
    if not getattr(operator, "initialized", False):
        return

    if operator.max_float < operator.min_float:
        operator.min_float, operator.max_float = operator.max_float, operator.min_float

def on_soft_min_max_float_update(operator, _context):
    if not getattr(operator, "initialized", False):
        return

    if operator.soft_max_float < operator.soft_min_float:
        operator.soft_min_float, operator.soft_max_float = operator.soft_max_float, operator.soft_min_float

def on_min_max_int_update(operator, _context):
    if not getattr(operator, "initialized", False):
        return

    if operator.max_int < operator.min_int:
        operator.min_int, operator.max_int = operator.max_int, operator.min_int

def on_soft_min_max_int_update(operator, _context):
    if not getattr(operator, "initialized", False):
        return

    if operator.soft_max_int < operator.soft_min_int:
        operator.soft_min_int, operator.soft_max_int = operator.soft_max_int, operator.soft_min_int