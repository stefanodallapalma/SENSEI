# Standard
import os

# Third party imports
from flask import request, Response, json

# Local application imports
import modules.software_quality.projects.projects as projects
from modules.software_quality.projects.known_datasets.KnownDataset import KnownDataset
from database.anita.controller.SonarqubeController import SonarqubeController
import utils.FileUtils as utils


def load_new_project():
    # Parameters - Required
    project_name = request.form["project_name"]
    project_zip = request.files["project_zip"]

    # Parameters - Optional
    known_dataset = None
    if "known_dataset" in request.form:
        known_dataset = request.form["known_dataset"]

    # noinspection PyBroadException
    try:
        results = projects.load_data(project_name, project_zip, known_dataset, new_project=True)
    except:
        return Response(json.dumps({"error": {"msg": "Internal server error"}}),
                        status=500, mimetype="application/json")

    status = results["status"]
    del results["status"]
    content = dict(results)

    if status < 400:
        content = results["content"]

    return Response(json.dumps(content), status=status, mimetype="application/json")


def delete_projects():
    project_list = request.form.getlist("project_list")

    msg = []
    for project in project_list:
        # noinspection PyBroadException
        try:
            results = projects.delete_project(project)
        except:
            return Response(json.dumps({"error": {"msg": "Internal server error"}}),
                            status=500, mimetype="application/json")

        status = results["status"]
        if status == 500:
            del results["status"]
            return Response(json.dumps(results), status=500, mimetype="application/json")
        elif status == 404:
            msg.append(project + ": " + results["error"]["msg"])

    if not msg:
        return Response(status=204)

    return Response(json.dumps({"error": {"msg": msg}}), status=404, mimetype="application/json")


def get_project():
    project_name = request.values["project_name"]
    sq_table = SonarqubeController()

    beans = sq_table.select_by_project_name(project_name)
    json_beans_list = [bean.json() for bean in beans]

    return Response(json.dumps(json_beans_list, sort_keys=False), status=200, mimetype="application/json")


def update_project():
    # Parameters - Required
    project_name = request.values["project_name"]
    project_zip = request.files["project_zip"]

    results = projects.load_data(project_name, project_zip, new_project=False)
    status = results["status"]
    del results["status"]
    content = dict(results)

    if status < 400:
        content = results["content"]

    return Response(json.dumps(content), status=status, mimetype="application/json")


def delete_project():
    project_name = request.values["project_name"]

    # noinspection PyBroadException
    try:
        results = projects.delete_project(project_name)
    except:
        return Response(json.dumps({"error": {"msg": "Internal server error"}}),
                        status=500, mimetype="application/json")

    status = results["status"]
    if status == 204:
        return Response(status=204)

    del results["status"]

    return Response(json.dumps(results), status=status, mimetype="application/json")


def get_known_projects():
    known_dataset = KnownDataset()
    path = known_dataset.path

    if os.path.exists(path) and os.path.isdir(path):
        dirs = utils.getdirs(path)
        return Response(json.dumps(dirs), status=200, mimetype="application/json")

    msg = "Internal access error. Impossible retrieve information about the known datasets stored"
    return Response(json.dumps({"error": msg}), status=200, mimetype="application/json")
