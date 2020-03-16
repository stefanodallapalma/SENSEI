# Third party imports
from flask import request, Response, json

# Local application imports
from modules.software_quality.experimentation.experimentation_enum import ExperimentationList


def get_experimentation_list():
    experimentations = []
    for experimentation in ExperimentationList:
        name = experimentation.value
        id = experimentation.name.split("_")[1]

        exp_dict = {"name": name, "id": id}
        experimentations.append(exp_dict)

    return Response(json.dumps(experimentations), status=200, mimetype="application/json")


def run_experimentation(project_name, experimentation_id):
    return Response(json.dumps("TO DO"), status=500, mimetype="application/json")


def experimentation_status(project_name, experimentation_id):
    return Response(json.dumps("TO DO"), status=500, mimetype="application/json")