def count_errors(errors):
    result = 0
    for error_list in errors.values():
        result += len(error_list)
    return result


def remove_empty_errors(errors):
    for key, value in list(errors.items()):
        if not value:
            del errors[key]
