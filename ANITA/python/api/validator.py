from datetime import datetime


def timestamp_validator(timestamp):
    type = timestamp_type(timestamp)

    if type is None:
        return False

    return True


def timestamp_type(timestamp):
    try:
        int(timestamp)
        return "int"
    except ValueError:
        pass

    try:
        float(timestamp)
        return "float"
    except ValueError:
        pass

    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return "date"
    except ValueError:
        pass

    return None