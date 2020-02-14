from flask import Response, json
import sonar.SonarqubeAPI as sq_api
import utils.SonarqubeUtils as sq_utils

from exception.NoProjectException import NoProjectException

html_pages_path = "../resources/html_pages/"

def create_project(name, project_key):
    project = sq_utils.get_project("Name", name)

    static_dict = {"name": name, "key": project_key}

    total_files = project["TotalFiles"]
    project_size = project["ProjectSize"]
    project_numbers = (total_files // project_size) + 1

    final_response = None
    for i in range(project_numbers):
        new_name = name + "_" + str(i + 1)
        new_project_key = project_key + "_" + str(i + 1)

        response = sq_api.create_project(new_name, new_project_key)

        if response.status_code >= 300:
            return Response(response.json(), status=response.status_code, mimetype="application/json")

        final_response = response

    response_dict = final_response.json()
    response_dict["project"].update(static_dict)

    return Response(json.dumps(response_dict), status=final_response.status_code, mimetype="application/json")


def delete_project(project_key):
    project = sq_utils.get_project("Key", project_key)

    total_files = project["TotalFiles"]
    project_size = project["ProjectSize"]
    project_numbers = (total_files // project_size) + 1

    error_msg_list = []
    for i in range(project_numbers):
        new_project_key = project_key + "_" + str(i + 1)
        response = sq_api.delete_project(new_project_key)

        if response.status_code >= 400:
            error_msg_list.append(response.json()["errors"])

    if not error_msg_list:
        content = "Successfull"
        status_code = 200
    else:
        content = error_msg_list
        status_code = 400

    return Response(json.dumps(content), status=status_code, mimetype="application/json")


def measures(project_key, metric_normalized, page_number=1):
    project = sq_utils.get_project("Key", project_key)

    total_files = project["TotalFiles"]
    project_size = project["ProjectSize"]
    project_numbers = (total_files // project_size) + 1

    total_files_analyzed = 0

    final_response_json = {}
    component_list = []

    missed_projects = []
    for i in range(project_numbers):
        print(str(i+1))

        new_project_key = project_key + "_" + str(i+1)
        response = sq_api.measures(new_project_key, metric_normalized, page_number)
        response_json = response.json()

        if not response_json["components"]:
            actual_key_split = response_json["baseComponent"]["key"].split("_")
            missed_project = "".join(actual_key_split[len(actual_key_split) - 1:])
            missed_projects.append(missed_project)

        total_files_analyzed += response_json["paging"]["total"]
        final_response_json.update(response_json)

        component_list += response_json["components"]

    # Update
    final_response_json["paging"]["total"] = total_files_analyzed
    final_response_json["baseComponent"]["key"] = project_key
    final_response_json["baseComponent"]["name"] = project["Name"]
    final_response_json["components"] = component_list

    return Response(json.dumps(final_response_json), status=200, mimetype="application/json")


def task_list(project_key):
    project = sq_utils.get_project("Key", project_key)

    total_files = project["TotalFiles"]
    project_size = project["ProjectSize"]
    project_numbers = (total_files // project_size) + 1

    responses = []
    for i in range(project_numbers):
        new_project_key = project_key + "_" + str(i + 1)
        response = sq_api.task_list(new_project_key)
        responses.append(response)

    return responses


def metric_list():
    return sq_api.metric_list()


def get_content(response):
    return json.loads(response.get_data(as_text=True))