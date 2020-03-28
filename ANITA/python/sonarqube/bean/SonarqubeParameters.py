import json


class SonarqubeParameters:
    def __init__(self, json_file):
        self._data = json_file

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def host(self):
        return self._data["host"]

    @host.setter
    def host(self, host):
        self._data["host"] = host

    @property
    def port(self):
        return self._data["port"]

    @port.setter
    def port(self, port):
        self._data["port"] = port

    @property
    def url(self):
        if self._data["host"].startswith("http"):
            return self._data["host"] + ":" + self._data["port"]

        return "http://" + self._data["host"] + ":" + self._data["port"]

    @property
    def token(self):
        return self._data["token"]

    @token.setter
    def token(self, token):
        self._data["token"] = token

    @property
    def user(self):
        return self._data["user"]

    @user.setter
    def user(self, user):
        self._data["user"] = user

    @property
    def password(self):
        return self._data["password"]

    @password.setter
    def password(self, password):
        self._data["password"] = password

    @property
    def projects(self):
        return self._data["projects"]

    @projects.setter
    def projects(self, projects):
        self._data["projects"] = projects

    def __str__(self):
        return_str = ""
        return_str += "HOST: " + self.host + "\n"
        return_str += "PORT: " + self.port + "\n"
        return_str += "URL: " + self.url + "\n"
        return_str += "USER: " + self.user + "\n"
        return_str += "PASSWORD: " + self.password + "\n"
        return_str += "TOKEN: " + self.token + "\n"
        return_str += "PROJECTS: " + str(self.projects)

        return return_str
