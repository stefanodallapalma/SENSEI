import requests, json
from requests.auth import HTTPBasicAuth
from utils.SonarqubeUtils import get_sonarqube_properties as properties

def create_project(name, project_key):
    api_url = "/api/projects/create"

    # Parameter setup
    param = {}
    param["project"] = project_key
    param["name"] = name

    sonarqube_parameters = properties()
    url = sonarqube_parameters.url + api_url
    response = requests.post(url, param)

    return response

def delete_project(project_key):
    api_url = "/api/projects/delete"

    # Parameter setup
    param = {}
    param["project"] = project_key

    sonarqube_parameters = properties()
    url = sonarqube_parameters.url + api_url

    # Basic Auth parameters
    user = sonarqube_parameters.user
    password = sonarqube_parameters.password

    response = requests.post(url, data=param, auth=HTTPBasicAuth(user, password))

    return response

