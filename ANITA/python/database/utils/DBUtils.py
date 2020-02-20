import json
from os.path import join
from database.db.DBType import DBType
from database.utils.DBParametersBean import DBParametersBean
from utils.FileUtils import load_json, save_json

res_db_path = "../resources/database/"
mysql_name = "mysql.json"


def get_db_parameters(db_type):
    if db_type == DBType.MYSQL:
        path = join(res_db_path, mysql_name)

    data = load_json(path)

    return DBParametersBean(data)


def add_database_name(db_type, database_name):
    if db_type == DBType.MYSQL:
        path = join(res_db_path, mysql_name)

    data = load_json(path)
    db_param = DBParametersBean(data)
    db_param.database_name = database_name

    save_json(path, db_param.data)