from flask import request, Response, json
from database.anita.table.SonarqubeTable import SonarqubeTable


def get_project():
    project_name = request.values["project_name"]
    sq_table = SonarqubeTable()

    beans = sq_table.select_by_project_name(project_name)
    json_beans_list = [bean.json() for bean in beans]

    return Response(json.dumps(json_beans_list, sort_keys=False), status=200, mimetype="application/json")
