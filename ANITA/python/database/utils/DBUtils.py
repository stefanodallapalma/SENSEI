import json
from os.path import join
from database.db.DBType import DBType
from database.utils.DBParametersBean import DBParametersBean

res_db_path = "../resources/db/"


def get_db_parameters(db_type):
    if db_type == DBType.MYSQL:
        path = join(res_db_path, "mysql.json")

    with open(path) as json_file:
        data = json.loads(json_file.read())

    return DBParametersBean(data)
