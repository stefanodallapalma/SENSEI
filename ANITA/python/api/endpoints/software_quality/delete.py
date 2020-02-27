from flask import request, Response, json
import shutil, os
from database.anita.table.SonarqubeTable import SonarqubeTable
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from sonarqube.utils import SonarqubeUtils as sq_utils


def delete_project():
    project_name = request.values["project_name"]

    status_dict = {}

    # Database
    sq_table = SonarqubeTable()
    if not sq_table.exist():
        status_dict["DB"] = False
    else:
        sq_table.delete_by_project_name(project_name)
        status_dict["DB"] = True

    # Local
    sq_local = SonarqubeLocalProject(project_name)
    if os.path.exists(sq_local.project_path):
        shutil.rmtree(sq_local.project_path)
        status_dict["Local"] = True
    else:
        status_dict["Local"] = False

    # Sonarqube json
    sq_utils.delete_project(project_name)
    status_dict["Updated projects json"] = True

    msg = {"status": status_dict}
    return Response(json.dumps(msg), status=200, mimetype="application/json")


def delete_projects():
    project_list = request.form.getlist("project_list")

    status = {}
    for project in project_list:
        response = delete_project()
        content_status = SonarqubeAPIExtended.get_json_content(response)["status"]

        status[project] = content_status

    msg = {"status": status}

    return Response(json.dumps(msg), status=200, mimetype="application/json")


def delete_pages():
    project_name = request.form["project_name"]
    rows = request.form.getlist["rows"]

    print(project_name)
    for row in rows:
        print(row)

