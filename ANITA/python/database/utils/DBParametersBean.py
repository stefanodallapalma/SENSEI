import json


class DBParametersBean():
    def __init__(self, json_file):
        self._data = json.loads(json_file.read())

    @property
    def host(self):
        return self._data["host"]

    @property
    def port(self):
        return self._data["port"]

    @property
    def user(self):
        return self._data["user"]

    @property
    def password(self):
        return self._data["password"]

    @property
    def database_name(self):
        return self._data["database_name"]