from functools import wraps


def is_required(value):
    if value is None:
        raise ValueError('Value is required')


def is_not_required_validator(validator):
    @wraps(validator)
    def wrapper(value):
        if value:
            validator(value)

    return wrapper


@is_not_required_validator
def is_2d(value):
    measurement = list(value)
    if len(measurement) == 2 and not all(isinstance(part, int) for part in measurement):
        raise ValueError('Value must be 2d measurement(tuple(int, int))')


@is_not_required_validator
def is_rgb_color(value):
    measurement = list(value)
    if len(measurement) == 3 and not all(isinstance(part, int) for part in measurement):
        raise ValueError('Value must be RGB color(tuple(int, int, int))')


@is_not_required_validator
def is_rgba_color(value):
    measurement = list(value)
    if len(measurement) == 4 and not all(isinstance(part, int) for part in measurement):
        raise ValueError('Value must be RGB color(tuple(int, int, int))')

