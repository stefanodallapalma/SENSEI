from utils.PortScanner import scanner
from sonarqube.utils import SonarqubeUtils as sq_utils
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from check.setup import *
from check.servers import run_sonarnet
from os.path import join, exists
import os
from database.anita.AnitaDB import AnitaDB
from database.utils import DBUtils as db_utils
from database.db.structure.DBType import DBType

resource_path = "../resources/"
database_resource_path = join(resource_path, "database")
sonarscanner_path = join(resource_path, "sonar-scanner")
mysql_name = "mysql.json"
sonarqube_name = "sonarqube_properties.json"
default_name = "default.json"


def check_preconditions():
    print("PRECONDITION CHECKING\n")

    # Resource folders
    folders = resource_precondition()
    if folders:
        print("Resource folders: OK (" + str(folders) + " created)")
    else:
        print("Resource folders: OK")

    print()

    # MySQL parameters
    mysql_property_path = join(database_resource_path, mysql_name)
    if not exists(mysql_property_path):
        print("MySQL parameters: File not found. Starting mysql setup")
        mysql_setup()
    else:
        print("MySQL parameters: OK")

    print()

    # Mysql connection test
    mysql_property = db_utils.get_db_parameters(DBType.MYSQL)
    if not scanner(mysql_property.host, mysql_property.port):
        print("MySQL server status: UNREACHABLE. Please check the status of the server and try again")
        return False
    else:
        print("MySQL server status: OK")

    print()

    # MySQL database
    db = AnitaDB(anonymous=True)
    if db.exist():
        print("MySQL ANITA DB: OK")
    else:
        print("MySQL ANITA DB: not found. Creation of a new db")
        db.create()
        db_utils.add_database_name(DBType.MYSQL, db.database_name)

    print()

    # Sonarqube parameters
    sonarqube_property_path = join(resource_path, sonarqube_name)
    if not exists(sonarqube_property_path):
        print("Sonarqube parameters: file not found. Starting sonarqube setup")
        sonarqube_setup()
    else:
        print("Sonarqube parameters: OK")

    print()

    # Sonarqube connection test
    sonarqube_property = sq_utils.get_sonarqube_properties()
    if not scanner(sonarqube_property.host, sonarqube_property.port):
        if sonarqube_property.host == "127.0.0.1":
            run_sonarnet()
            if not scanner(sonarqube_property.host, sonarqube_property.port):
                print("Sonarqube server status: UNREACHABLE. Please check the status of the server and try again")
                return False
            else:
                print("Sonarqube server status: OK")
        else:
            print("Sonarqube server status: UNREACHABLE. Please check the status of the server and try again")
            return False
    else:
        print("Sonarqube server status: OK")

    print()

    # Sonarqube token
    server_sq = SonarqubeAPIExtended()
    if sonarqube_property.token == "":
        print("Sonarqube token not found: generation of a new one")
        response = server_sq.generate_token(sonarqube_property.user, "ANITA")
        content = server_sq.get_json_content(response)
        print(content)
        sq_utils.set_token(content["token"])
        print()

    # Sonarscanner
    dirs = [f for f in os.listdir(sonarscanner_path) if os.path.isdir(join(sonarscanner_path, f))]
    if not dirs:
        print("Sonar-scanner status: not found. Sonar-scanner will be installed in a few seconds")
        zip_path = download()
        extract_content(zip_path, "sonar-scanner")
        os.remove(zip_path)
        print("\nSonar-scanner has been installed successfully")
    else:
        print("Sonar-scanner status: OK")

    print()

    return True


def resource_precondition():
    # Resource dir names
    dirs = ["html_pages", "zip", "database", "sonar-scanner"]

    # Resource direcories
    onlydirs = [f for f in os.listdir(resource_path) if os.path.isdir(join(resource_path, f))]

    folders_created = []
    for dir in dirs:
        if dir not in onlydirs:
            os.mkdir(os.path.join(resource_path, dir))
            folders_created.append(dir)

    return folders_created


