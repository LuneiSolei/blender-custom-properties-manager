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

def on_array_length_update(operator_instance, _context):
    if not getattr(operator_instance, "initialized", False):
        return

    collection = operator_instance.default_array
    new_length = operator_instance.array_length
    current_length = len(collection)

    if new_length > current_length:
        for _ in range(new_length - current_length):
            collection.add()
    elif new_length < current_length:
        for _ in range(current_length - new_length):
            collection.remove(len(collection) - 1)