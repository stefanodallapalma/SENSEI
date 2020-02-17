import json, os
from sonar.bean.SonarqubeParameters import SonarqubeParameters

from exception.NoProjectException import NoProjectException
from exception.DuplicateProjectNameException import DuplicateProjectNameException
from exception.DuplicateProjectKeyException import DuplicateProjectKeyException


sonarqube_setup_path = "../resources/sonarqube_properties.json"
html_pages_path = "../resources/html_pages/"
jsonbuffer_suffix = "_infoBuffer.json"

def get_sonarqube_properties():
    return SonarqubeParameters(sonarqube_setup_path)


def add_project(name, projectkey, number_of_files, project_size):
    sq_parameters = SonarqubeParameters(sonarqube_setup_path)

    projects = sq_parameters.projects

    # Check if the name and project key are already in the json
    for project in projects:
        if project["Name"] == name:
            raise DuplicateProjectNameException()
        elif project["Key"] == projectkey:
            raise DuplicateProjectKeyException()

    project_dict = {}
    project_dict["Name"] = name
    project_dict["Key"] = projectkey
    project_dict["TotalFiles"] = number_of_files
    project_dict["ProjectSize"] = project_size

    projects.append(project_dict)

    sq_parameters.projects = projects

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sq_parameters.data, outfile)


def delete_project(name):
    sq_parameters = SonarqubeParameters(sonarqube_setup_path)

    projects = sq_parameters.projects

    for project in projects:
        if project["Name"] == name:
            projects.remove(project)
            break

    sq_parameters.projects = projects

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sq_parameters.data, outfile)


def get_project_key(name):
    sq_parameters = SonarqubeParameters(sonarqube_setup_path)
    projects = sq_parameters.projects

    for project in projects:
        if project["Name"] == name:
            return project["Key"]

    raise NoProjectException()


def get_name(project_key):
    sq_parameters = SonarqubeParameters(sonarqube_setup_path)
    projects = sq_parameters.projects

    # Check if the project key is already in the json
    for project in projects:
        if project["Key"] == project_key:
            return project["Name"]

    raise NoProjectException()


def get_auth():
    sq_parameters = get_sonarqube_properties()
    user = sq_parameters.user
    psw = sq_parameters.password

    return user, psw


def get_project(key, value):
    """
    Get the project with the value of a proper key
    """

    sq_parameter = get_sonarqube_properties()

    projects = sq_parameter.projects

    for project in projects:
        if project[key] == value:
            return project

    raise NoProjectException("EXC")


def set_token(token):
    sq_parameters = SonarqubeParameters(sonarqube_setup_path)
    sq_parameters.token = token

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sq_parameters.data, outfile)


def get_bufferlist(name):
    project_path = os.path.join(html_pages_path, name)
    projectbufferjson_path = os.path.join(project_path, (name + jsonbuffer_suffix))

    with open(projectbufferjson_path) as json_file:
        buffers = json.loads(json_file.read())

    return buffers