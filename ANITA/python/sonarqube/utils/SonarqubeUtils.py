import json, os, random, string
from sonarqube.bean.SonarqubeParameters import SonarqubeParameters

from exceptions import NoProjectException, DuplicateProjectException

sonarqube_setup_path = "../resources/sonarqube_properties.json"


def get_sonarqube_properties():
    with open(sonarqube_setup_path) as json_file:
        data = json.loads(json_file.read())

    return SonarqubeParameters(data)


def add_project(name, project_key, number_of_files, project_size):
    # Precondition
    if project_exist(project_key, name):
        raise DuplicateProjectException()

    sq_parameters = get_sonarqube_properties()
    projects = sq_parameters.projects

    project_dict = {"Name": name, "Key": project_key, "TotalFiles": number_of_files, "ProjectSize": project_size}
    projects.append(project_dict)

    sq_parameters.projects = projects

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sq_parameters.data, outfile)


def delete_project(name):
    sq_parameters = get_sonarqube_properties()

    projects = sq_parameters.projects

    for project in projects:
        if project["Name"] == name:
            projects.remove(project)
            break

    sq_parameters.projects = projects

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sq_parameters.data, outfile)


def generate_project_key(min_length=10, max_length=50):
    MAX_ATTEMPTS = 1000
    attempt = 1

    project_key = None
    letters = string.ascii_lowercase

    while project_key is None and attempt < MAX_ATTEMPTS:
        key_length = random.randint(min_length, max_length)
        project_key = ''.join(random.choice(letters) for i in range(key_length))
        attempt += 1

        if project_exist(project_key):
            project_key = None

    if project_key is None:
        raise DuplicateProjectException()

    return project_key


def get_project_key(name):
    sq_parameters = get_sonarqube_properties()
    projects = sq_parameters.projects

    for project in projects:
        if project["Name"] == name:
            return project["Key"]

    raise NoProjectException()


def get_name(project_key):
    sq_parameters = get_sonarqube_properties()
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


def project_exist(project_key, name=None):
    sq_parameters = get_sonarqube_properties()
    projects = sq_parameters.projects

    for project in projects:
        if project["Key"] == project_key:
            return True
        if name is not None and project["Name"] == name:
            return True

    return False


def set_token(token):
    sq_parameters = get_sonarqube_properties()
    sq_parameters.token = token

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sq_parameters.data, outfile)
