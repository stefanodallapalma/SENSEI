from flask import request, Response, json
import sonarqube.utils.SonarqubeUtils as sq_utils
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
import shutil
from os.path import join

from exception.NoProjectException import NoProjectException

html_pages_path = "../resources/html_pages/"

def delete():
    server_sq = SonarqubeAPIExtended()
    sonar_properties = sq_utils.get_sonarqube_properties()
    project_error_list = []

    # Take the BasicAuth for the authentication
    user = sonar_properties.user
    password = sonar_properties.password

    project_list = request.form.getlist("project_list")
    print(str(project_list))

    if not project_list:
        return Response(json.dumps("There are no projects to delete in the request parameters"),
                        status=200, mimetype="application/json")

    for project in project_list:
        try:
            # Take the project key from its project name
            project_key = sq_utils.get_project_key(project)
            print("Project to delete: " + project)
            print("Project key: " + project_key)

            delete_response = server_sq.delete_project(project_key)
            print("Delete response status code: " + str(delete_response.status_code))

            if 400 <= delete_response.status_code < 500:
                print(str(SonarqubeAPIExtended.get_json_content(delete_response)))

            # Remove the project key from the sonarqube json
            sq_utils.delete_project(project)

            # Delete project folder
            project_path = join(html_pages_path, project)
            shutil.rmtree(project_path)
        except NoProjectException:
            project_error_list.append(project)

    if not project_error_list:
        json_response = json.dumps("Operation successfully")
        status_code = 200
    else:
        dict_response = {}
        dict_response["Message"] = "There are different projects that are not been deleted " \
                                   "because there are no project keys connected to them: " + str(project_error_list)
        json_response = json.dumps(dict_response)
        status_code = 201

    return Response(json_response, status=status_code, mimetype="application/json")