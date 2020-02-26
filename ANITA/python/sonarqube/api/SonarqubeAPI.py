import requests
from flask import Response, json
from requests.auth import HTTPBasicAuth
from sonarqube.utils.SonarqubeUtils import get_sonarqube_properties

class SonarqubeAPI:
    def __init__(self):
        self._parameters = get_sonarqube_properties()

    def create_project(self, name, project_key):
        api_url = "/api/projects/create"

        # Parameter setup
        param = {"project": project_key, "name": name}

        url = self._parameters.url + api_url
        response = requests.post(url, param)

        return Response(response.content, response.status_code, response.headers.items())

    def delete_project(self, project_key):
        api_url = "/api/projects/delete"

        # Parameter setup
        param = {"project": project_key}

        url = self._parameters.url + api_url

        # Basic Auth parameters3
        user = self._parameters.user
        password = self._parameters.password

        response = requests.post(url, data=param, auth=HTTPBasicAuth(user, password))

        return Response(response.content, response.status_code, response.headers.items())

    def measures(self, project_key, metrics, page_number = 0):
        api = "/api/measures/component_tree"

        url = self._parameters.url + api + "?metricKeys=" + metrics + "&component=" + project_key
        if page_number > 0:
            url += "&p=" + str(page_number)

        response = requests.get(url)

        return Response(response.content, response.status_code, response.headers.items())

    def tasks(self, project_key):
        api = "/api/ce/component"

        url = self._parameters.url + api + "?component=" + project_key

        response = requests.get(url)

        return Response(response.content, response.status_code, response.headers.items())

    def metrics(self):
        api = "/api/metrics/search"

        url = self._parameters.url + api

        response = requests.get(url)

        return Response(response.content, response.status_code, response.headers.items())

    def generate_token(self, login, name):
        api = "/api/user_tokens/generate"

        # Parameter setup
        param = {"login": login, "name": name}

        url = self._parameters.url + api

        # Basic Auth parameters
        user = self._parameters.user
        password = self._parameters.password

        response = requests.post(url, data=param, auth=HTTPBasicAuth(user, password))

        return Response(response.content, response.status_code, response.headers.items())

    @staticmethod
    def get_json_content(response):
        return json.loads(response.get_data(as_text=True))
