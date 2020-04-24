import time
from datetime import datetime


def timestamp_validator(name):
    # Timestamp
    try:
        timestamp = int(name)
        if timestamp > int(datetime.now().timestamp()) or timestamp < 0:
            raise Exception("Timestamp out of range")

        return timestamp
    except:
        pass

    # Date
    # If contains millisec, remove it
    if "." in name:
        name = name.split(".")[0]

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H-%M-%S",
        "%Y-%m-%d %H_%M_%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H-%M-%S",
        "%Y-%m-%dT%H_%M_%S",
    ]

    for fmt in formats:
        try:
            timestamp = int(time.mktime(datetime.strptime(name, fmt).timetuple()))
            return timestamp
        except ValueError:
            pass

    raise Exception("Invalid name format")