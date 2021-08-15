def _snake_to_camel(x):
    components = x.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def count_errors(errors):
    result = 0
    for error_list in errors.values():
        result += len(error_list)
    return result


def get_errors(errors, field_name):
    return errors.setdefault(field_name, [])


def reformat_errors(errors):
    result = {}
    for key, value in list(errors.items()):
        if value:
            result[_snake_to_camel(key)] = value
    return result
