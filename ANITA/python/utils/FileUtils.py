import os
import json


def get_dict_from_file(path):
    file = open(path, 'r')

    parameters = {}
    for line in file:
        split = line.split(":")
        parameters[split[0].lstrip()] = split[1].rstrip()

    return parameters


def getfiles(dir_path, abs_path=False, ext_filter=None, recursive=False):
    if not recursive:
        onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    else:
        onlyfiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_path) for f in filenames if
              os.path.isfile(os.path.join(dp, f))]

    if abs_path:
        if not recursive:
            onlyfiles = [os.path.join(dir_path, f) for f in onlyfiles]
        else:
            onlyfiles = [os.path.abspath(f) for f in onlyfiles]

    if ext_filter is not None:
        if isinstance(ext_filter, (tuple, list, str)):
            if isinstance(ext_filter, (list, str)):
                ext_filter = tuple(ext_filter)

            onlyfiles = [file for file in onlyfiles if file.endswith(ext_filter)]
        else:
            raise Exception("The extensions list must be of type list or tuple")

    return onlyfiles


def getdirs(dir_path, abs_path=False):
    onlydirs = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
    if abs_path:
        onlydirs = [os.path.join(dir_path, f) for f in onlydirs]

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