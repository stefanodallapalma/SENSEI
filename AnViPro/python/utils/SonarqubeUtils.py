import json
from sonar.bean.SonarqubeParameters import SonarqubeParameters

from exception.NoProjectException import NoProjectException
from exception.DuplicateProjectNameException import DuplicateProjectNameException
from exception.DuplicateProjectKeyException import DuplicateProjectKeyException

sonarqube_setup_path = "../resources/sonarqube_properties.json"

def get_sonarqube_properties():
    return SonarqubeParameters(sonarqube_setup_path)

def add_project(name, projectkey, overwrite_name=False):
    sonarqubeParameters = SonarqubeParameters(sonarqube_setup_path)

    projectKeys = sonarqubeParameters.projectKeys

    if name in projectKeys and overwrite_name is False:
        raise DuplicateProjectNameException()

    if projectkey in projectKeys.values():
        raise DuplicateProjectKeyException()

    projectKeys[name] = projectkey
    sonarqubeParameters.projectKeys = projectKeys

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sonarqubeParameters.data, outfile)

def delete_project(name):
    sonarqubeParameters = SonarqubeParameters(sonarqube_setup_path)

    projectKeys = sonarqubeParameters.projectKeys

    if name in projectKeys:
        del projectKeys[name]

    sonarqubeParameters.projectKeys = projectKeys

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sonarqubeParameters.data, outfile)

def get_project_key(name):
    sonarqubeParameters = SonarqubeParameters(sonarqube_setup_path)
    projectKeys =sonarqubeParameters.projectKeys

    if name not in projectKeys:
        raise NoProjectException()

    return projectKeys[name]

def get_auth():
    sonarqube_properties = get_sonarqube_properties()
    user = sonarqube_properties.user
    psw = sonarqube_properties.password

    return user, psw

