# Standard
import datetime
import logging
import traceback

# Third party imports
from flask import request, Response, json

import modules.software_quality.projects.projects as projects
from database.anita.controller.SonarqubeController import SonarqubeController
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
# Local application imports
from ...validator import *

logger = logging.getLogger("Projects endpoints")


# Project
def get_project(project_name):
    logger.info("Endpoint Project (GET): START")

    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if project_name is None or not sq_local.exist():
        # LOG
        if project_name is None:
            logger.debug("Project None")
        else:
            logger.debug("Project " + project_name + " not found")
        logger.info("Endpoint Project (PUT): END")
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    # Retrieve info on the db
    sq_table = SonarqubeController()

    try:
        beans = sq_table.select_by_project_name(project_name)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project (GET): END")
    return Response(json.dumps(beans, sort_keys=False), status=200, mimetype="application/json")


def load_new_project(project_name):
    logger.info("Endpoint Project (POST): START")
    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if sq_local.exist():
        logger.debug("Project " + project_name + " already created")
        logger.info("Endpoint Project (POST): END")
        return Response(json.dumps({"error": "Project already created"}), status=400, mimetype="application/json")

    project_zip = request.files["project_zip"]

    # Parameters - Optional
    additional_info = request.form["additional_info"]
    if additional_info.upper() == "FALSE":
        additional_info = False
    else:
        additional_info = True

    try:
        status, content = projects.load_data(project_name, project_zip, additional_info=additional_info,
                                             new_project=True)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project (POST): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    if status >= 400:
        logger.info("Endpoint Project (POST): END")
        return Response(json.dumps(content), status=status, mimetype="application/json")

    logger.info("Endpoint Project (POST): END")
    return Response(json.dumps(content), status=202, mimetype="application/json")


def update_project(project_name):
    logger.info("Endpoint Project (PUT): START")

    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if project_name is None or not sq_local.exist():
        # LOG
        if project_name is None:
            logger.debug("Project None")
        else:
            logger.debug("Project " + project_name + " not found")
        logger.info("Endpoint Project (PUT): END")
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    # Parameters - Required
    project_zip = request.files["project_zip"]

    try:
        status, content = projects.load_data(project_name, project_zip)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project (PUT): END")

    if status >= 400:
        return Response(json.dumps(content), status=status, mimetype="application/json")

    return Response(json.dumps(content), status=202, mimetype="application/json")


def delete_project(project_name):
    logger.info("Endpoint Project (DELETE): START")

    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if project_name is None or not sq_local.exist():
        # LOG
        if project_name is None:
            logger.debug("Project None")
        else:
            logger.debug("Project " + project_name + " not found")
        logger.info("Endpoint Project (DELETE): END")
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    try:
        status, content = projects.delete_project(project_name)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project (DELETE): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project (DELETE): END")

    if status >= 400:
        return Response(json.dumps(content), status=status, mimetype="application/json")

    return Response(status=204)


def project_status_all(project_name):
    logger.info("Endpoint Project - Status (all): START")

    # Precondition
    sq_local = SonarqubeLocalProject(project_name)
    if not sq_local.exist():
        logger.debug("Project " + project_name + " not found")
        logger.info("Endpoint Project - Status (all): END")
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    dumps_status = {}
    try:
        status, content = projects.project_info(project_name)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Status (all): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    timestamps = content["dumps(timestamps)"]
    for timestamp in timestamps:
        try:
            status, content = projects.upload_task(project_name, timestamp)
        except Exception as e:
            logger.error("Internal server error")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            logger.info("Endpoint Project - Status (all): END")
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        dumps_status[date] = content

    logger.info("Endpoint Project - Status (all): END")
    return Response(json.dumps(dumps_status, sort_keys=False), status=200, mimetype="application/json")


def label(project_name):
    logger.info("Endpoint Project - Label: START")

    sq_local = SonarqubeLocalProject(project_name)
    if not sq_local.exist():
        logger.debug("Project " + project_name + " not found")
        logger.info("Endpoint Project - Label: END")
        return Response(json.dumps({"error": "Project not found"}), status=404, mimetype="application/json")

    label_csv = request.files["label_csv"]

    try:
        status, content = projects.add_label(project_name, label_csv)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Label: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Label: END")
    return Response(json.dumps(content), status=status, mimetype="application/json")


def project_status(project_name, timestamp):
    logger.info("Endpoint Project - Status: START")
    # Precondition
    if not timestamp_validator(timestamp):
        logger.debug("Invalid timestamp")
        logger.info("Endpoint Project - Status: END")
        return Response(json.dumps({"error": "Unprocessable entity: invalid timestamp"}), status=422,
                        mimetype="application/json")

    # noinspection PyBroadException
    try:
        status, content = projects.upload_task(project_name, timestamp)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Status: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Status: END")
    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")


def project_info(project_name):
    logger.info("Endpoint Project - Info: START")

    # noinspection PyBroadException
    try:
        status, content = projects.project_info(project_name)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Info: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Info: END")
    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")


# Projects
def projects_list():
    logger.info("Endpoint Projects - List: START")
    projects_list = projects.get_project_list()
    logger.info("Endpoint Projects - List: END")
    return Response(json.dumps(projects_list), status=200, mimetype="application/json")


def delete_projects():
    logger.info("Endpoint Projects - Delete: START")
    project_list = request.form.getlist("project_list")

    msg = []
    for project in project_list:
        # noinspection PyBroadException
        try:
            status, content = projects.delete_project(project)
        except Exception as e:
            logger.error("Internal server error")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            logger.info("Endpoint Projects - Delete: END")
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        if status == 500:
            logger.debug(str(content))
            logger.info("Endpoint Projects - Delete: END")
            return Response(json.dumps(content), status=500, mimetype="application/json")
        elif status == 404:
            msg.append(project + ": " + content["error"])

    logger.info("Endpoint Projects - Delete: END")

    if not msg:
        return Response(status=204)

    return Response(json.dumps({"errors": msg}), status=404, mimetype="application/json")


def projects_status():
    logger.info("Endpoint Projects - Status: START")

    project_names = projects.get_project_list()

    status_projects = {}
    for project_name in project_names:
        dumps_status = {}
        # noinspection PyBroadException
        try:
            status, content = projects.project_info(project_name)
        except Exception as e:
            logger.error("Internal server error")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            logger.info("Endpoint Projects - Delete: END")
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        timestamps = content["dumps(timestamps)"]
        for timestamp in timestamps:
            # noinspection PyBroadException
            try:
                status, content = projects.upload_task(project_name, timestamp)
            except Exception as e:
                logger.error("Internal server error")
                logger.error(str(e))
                logger.error(traceback.format_exc())
                logger.info("Endpoint Projects - Delete: END")
                error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
                return Response(json.dumps(error_content), status=500, mimetype="application/json")

            date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            dumps_status[date] = content

        status_projects[project_name] = dumps_status

    logger.info("Endpoint Projects - Delete: END")
    return Response(json.dumps(status_projects, sort_keys=False), status=200, mimetype="application/json")


def projects_info():
    logger.info("Endpoint Projects - Info: START")
    project_names = projects.get_project_list()

    info_projects = {}
    for project_name in project_names:
        # noinspection PyBroadException
        try:
            status, content = projects.project_info(project_name)
        except Exception as e:
            logger.error("Internal server error")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            logger.info("Endpoint Projects - Info: END")
            error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
            return Response(json.dumps(error_content), status=500, mimetype="application/json")

        info_projects[project_name] = content

    logger.info("Endpoint Projects - Info: END")
    return Response(json.dumps(info_projects), status=200, mimetype="application/json")
