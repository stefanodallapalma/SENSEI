from utils.FileUtils import load_json, save_json
from sonarscanner.SonarscannerUtils import *
from os.path import join

resource_folder = "../resources/"
database_resource_path = join(resource_folder, "database")
mysql_name = "mysql.json"
sonarqube_name = "sonarqube_properties.json"
default_name = "default.json"


def mysql_setup():
    choose = input("Internal or external setup? (I/E): ")

    if choose.upper() == "I":
        default_dict = load_json(join(resource_folder, default_name))
        host = default_dict["host"]
        if "https" in host:
            host = host.replace("https://", "")
        elif "http" in host:
            host = host.replace("http://", "")

        port = default_dict["mysql_port"]
        user = default_dict["mysql_user"]
        password = default_dict["mysql_password"]
    else:
        host = input("HOST: ")
        port = input("PORT")
        user = input("USER: ")
        password = input("PASSWORD: ")

    mysql_dict = {"host": host, "port": port, "user": user, "password": password, "database_name": ""}

    output_path = join(database_resource_path, "mysql.json")
    save_json(output_path, mysql_dict)


def sonarqube_setup():
    choose = input("Internal or external setup? (I/E): ")

    if choose.upper() == "I":
        default_dict = load_json(join(resource_folder, default_name))
        host = default_dict["host"]
        port = default_dict["sonarqube_port"]
        user = default_dict["sonarqube_user"]
        password = default_dict["sonarqube_password"]
    else:
        host = input("HOST: ")
        port = input("PORT")
        user = input("USER: ")
        password = input("PASSWORD: ")

    sonarqube_dict = {"host": host, "port": port, "user": user, "password": password, "token": "", "projects": []}

    output_path = join(resource_folder, sonarqube_name)
    save_json(output_path, sonarqube_dict)


def sonarscanner_setup():
    zip_path = download()
    extract_content(zip_path, "sonar-scanner")
    os.remove(zip_path)
