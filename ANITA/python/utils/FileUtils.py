import os
import json
def get_dict_from_file(path):
    file = open(path, 'r')

    parameters = {}
    for line in file:
        split = line.split(":")
        parameters[split[0].lstrip()] = split[1].rstrip()

    return parameters