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


def measures(project_key, metric_normalized, page_number = 0):
    api = "/api/measures/component_tree"

    sonarqube_parameters = properties()

    url = sonarqube_parameters.url + api + "?metricKeys=" + metric_normalized + "&component=" + project_key
    if page_number > 0:
        url += "&p=" + str(page_number)

    response = requests.get(url)

    return response


def task_list(project_key):
    api = "/api/ce/component"

    sonarqube_parameters = properties()
    url = sonarqube_parameters.url + api + "?component=" + project_key

    response = requests.get(url)

    return response

def metric_list():
    api = "/api/metrics/search"

    sonarqube_parameters = properties()
    url = sonarqube_parameters.url + api

    response = requests.get(url)

    return response


def generate_token(login, name):
    api = "/api/user_tokens/generate"

    # Parameter setup
    param = {}
    param["login"] = login
    param["name"] = name

    sonarqube_parameters = properties()
    url = sonarqube_parameters.url + api

    # Basic Auth parameters
    user = sonarqube_parameters.user
    password = sonarqube_parameters.password

    response = requests.post(url, data=param, auth=HTTPBasicAuth(user, password))

    return response