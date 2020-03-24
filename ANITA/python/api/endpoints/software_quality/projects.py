# Standard
import os, datetime, traceback
from datetime import datetime

# Third party imports
from celery.bin.control import control
from flask import request, Response, json

# Local application imports
from ...validator import *
import modules.software_quality.projects.projects as projects
from database.anita.controller.SonarqubeController import SonarqubeController
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
import utils.FileUtils as utils


# Project
def get_project(project_name):
    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if project_name is None or not sq_local.exist():
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    # Retrieve info on the db
    sq_table = SonarqubeController()

    # noinspection PyBroadException
    try:
        beans = sq_table.select_by_project_name(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(beans, sort_keys=False), status=200, mimetype="application/json")


def load_new_project(project_name):
    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if sq_local.exist():
        return Response(json.dumps({"error": "Project already created"}), status=400, mimetype="application/json")

    project_zip = request.files["project_zip"]

    # Parameters - Optional
    additional_info = request.form["additional_info"]
    if additional_info.upper() == "FALSE":
        additional_info = False
    else:
        additional_info = True

    # noinspection PyBroadException
    try:
        status, content = projects.load_data(project_name, project_zip, additional_info=additional_info,
                                             new_project=True)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    if status >= 400:
        return Response(json.dumps(content), status=status, mimetype="application/json")

    return Response(json.dumps(content), status=202, mimetype="application/json")


def update_project(project_name):
    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if project_name is None or not sq_local.exist():
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    # Parameters - Required
    project_zip = request.files["project_zip"]

    # noinspection PyBroadException
    try:
        status, content = projects.load_data(project_name, project_zip)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    if status >= 400:
        return Response(json.dumps(content), status=status, mimetype="application/json")

    return Response(json.dumps(content), status=202, mimetype="application/json")


def delete_project(project_name):
    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if project_name is None or not sq_local.exist():
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    # noinspection PyBroadException
    try:
        status, content = projects.delete_project(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    if status >= 400:
        return Response(json.dumps(content), status=status, mimetype="application/json")

    return Response(status=204)


def project_status_all(project_name):
    # Precondition
    sq_local = SonarqubeLocalProject(project_name)
    if not sq_local.exist():
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    dumps_status = {}
    # noinspection PyBroadException
    try:
        status, content = projects.project_info(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    timestamps = content["dumps(timestamps)"]
    for timestamp in timestamps:
        # noinspection PyBroadException
        try:
            status, content = projects.upload_task(project_name, int(timestamp))
        except Exception as e:
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        dumps_status[date] = content

    return Response(json.dumps(dumps_status, sort_keys=False), status=200, mimetype="application/json")


def label(project_name):
    sq_local = SonarqubeLocalProject(project_name)
    if not sq_local.exist():
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    label_csv = request.files["label_csv"]

    try:
        status, content = projects.add_label(project_name, label_csv)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content), status=status, mimetype="application/json")


def project_status(project_name, timestamp):
    # Precondition
    if not timestamp_validator(timestamp):
        return Response(json.dumps({"error": "Unprocessable entity: invalid timestamp"}), status=422,
                        mimetype="application/json")

    # noinspection PyBroadException
    try:
        status, content = projects.upload_task(project_name, timestamp)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")


def project_info(project_name):
    # noinspection PyBroadException
    try:
        status, content = projects.project_info(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")


# Projects
def projects_list():
    projects_list = projects.get_project_list()
    return Response(json.dumps(projects_list), status=200, mimetype="application/json")


def delete_projects():
    project_list = request.form.getlist("project_list")

    msg = []
    for project in project_list:
        # noinspection PyBroadException
        try:
            status, content = projects.delete_project(project)
        except Exception as e:
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        if status == 500:
            return Response(json.dumps(content), status=500, mimetype="application/json")
        elif status == 404:
            msg.append(project + ": " + content["error"])

    if not msg:
        return Response(status=204)

    return Response(json.dumps({"errors": msg}), status=404, mimetype="application/json")


def projects_status():
    project_names = projects.get_project_list()

    status_projects = {}
    for project_name in project_names:
        dumps_status = {}
        # noinspection PyBroadException
        try:
            status, content = projects.project_info(project_name)
        except Exception as e:
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        timestamps = content["dumps(timestamps)"]
        for timestamp in timestamps:
            # noinspection PyBroadException
            try:
                status, content = projects.upload_task(project_name, int(timestamp))
            except Exception as e:
                error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
                return Response(json.dumps(error_content), status=500, mimetype="application/json")

            date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            dumps_status[date] = content

        status_projects[project_name] = dumps_status

    return Response(json.dumps(status_projects, sort_keys=False), status=200, mimetype="application/json")


def projects_info():
    project_names = projects.get_project_list()

    info_projects = {}
    for project_name in project_names:
        # noinspection PyBroadException
        try:
            status, content = projects.project_info(project_name)
        except Exception as e:
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        info_projects[project_name] = content

    return Response(json.dumps(info_projects), status=200, mimetype="application/json")
