def parse_int(input_value, default_value=None) -> int:
    if input_value is None:
        return default_value
    try:
        return int(input_value)
    except ValueError:
        return default_value
