import json


def load_json(path):
    with open(path) as json_file:
        data = json.loads(json_file.read())

    return data
