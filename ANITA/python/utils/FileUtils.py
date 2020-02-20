import os
import json


def get_dict_from_file(path):
    file = open(path, 'r')

    parameters = {}
    for line in file:
        split = line.split(":")
        parameters[split[0].lstrip()] = split[1].rstrip()

    return parameters


def getfiles(dir_path):
    onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return onlyfiles


def getdirs(dir_path):
    onlydirs = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
    return onlydirs


def getparent_path(path):
    path = os.path.abspath(path)

    split = path.split(os.path.sep)

    if path.endswith(os.path.sep):
        split = split[:-2]
    else:
        split = split[:-1]

    parent_path = os.path.sep.join(split)

    return parent_path


def load_json(path):
    with open(path) as json_file:
        data = json.loads(json_file.read())

    return data


def save_json(path, file):
    with open(path, 'w') as outfile:
        json.dump(file, outfile)