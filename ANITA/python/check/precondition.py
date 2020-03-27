from utils.PortScanner import scanner
from sonarqube.utils import SonarqubeUtils as sq_utils
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from check.setup import *
from os.path import join, exists
import os, datetime, time
from database.anita.AnitaDB import AnitaDB
from database.utils import DBUtils as db_utils
from database.db.structure.DBType import DBType
from sonarqube.api.SonarqubeAPI import SonarqubeAPI

resource_path = "../resources/"
database_resource_path = join(resource_path, "database")
sonarscanner_path = join(resource_path, "sonar-scanner")
mysql_name = "mysql.json"
sonarqube_name = "sonarqube_properties.json"
default_name = "default.json"

LIMIT_TIME = 120     # sec


def check_preconditions():
    print("PRECONDITION CHECKING\n")

    # Resource folders
    folders = resource_precondition()
    if folders:
        print("Resource folders: OK (" + str(folders) + " created)")
    else:
        print("Resource folders: OK")

    # Parameters
    print("PARAMETERS")
    # Sonarqube parameters
    sonarqube_property_path = join(resource_path, sonarqube_name)
    if not exists(sonarqube_property_path):
        print("Sonarqube: parameters not found. Starting sonarqube setup")
        sonarqube_setup()
    print("Sonarqube: OK")

    # MySQL parameters
    mysql_property_path = join(database_resource_path, mysql_name)
    if not exists(mysql_property_path):
        print("MySQL: parameters not found. Starting mysql setup")
        mysql_setup()
    print("MySQL: OK")

    # Connection test
    print("CONNECTION TEST")

    # Mysql connection test
    mysql_property = db_utils.get_db_parameters(DBType.MYSQL)
    if not scanner(mysql_property.host, mysql_property.port):
        print("MySQL: waiting...")
        start = int(datetime.datetime.now().timestamp())
        actual = int(datetime.datetime.now().timestamp())
        while (actual - start) < LIMIT_TIME and scanner(mysql_property.host, mysql_property.port):
            time.sleep(1)
            actual = int(datetime.datetime.now().timestamp())

        if (actual - start) >= LIMIT_TIME:
            print("MySQL: server UNREACHABLE")
            return False
    print("MySQL server status: OK")

    # Sonarqube connection test
    sonarqube_property = sq_utils.get_sonarqube_properties()
    print(sonarqube_property.url)
    if not scanner(sonarqube_property.host, sonarqube_property.port):
        print("Sonarqube: waiting...")
        start = int(datetime.datetime.now().timestamp())
        actual = int(datetime.datetime.now().timestamp())
        while (actual - start) < LIMIT_TIME and scanner(sonarqube_property.host, sonarqube_property.port):
            time.sleep(1)
            actual = int(datetime.datetime.now().timestamp())

        if (actual - start) >= LIMIT_TIME:
            print("Sonarqube: server UNREACHABLE")
            return False
    print("Sonarqube: OK")

    print("Waiting that the server is up")
    # Wait that the server is up
    sq_api = SonarqubeAPI()
    response = sq_api.server_status()
    status = SonarqubeAPI.get_json_content(response)["status"]
    if status != "UP":
        print("Sonarqube: waiting... (server status: " + status + ")")
        start = int(datetime.datetime.now().timestamp())
        actual = int(datetime.datetime.now().timestamp())
        while (actual - start) < LIMIT_TIME and status != "UP":
            time.sleep(1)
            actual = int(datetime.datetime.now().timestamp())

        if (actual - start) >= LIMIT_TIME:
            print("Sonarqube: server not ready")
            return False

    # Database
    # MySQL database
    db = AnitaDB(anonymous=True)
    if db.exist():
        print("Database already created")
    else:
        print("Database not found. Creation of a new db")
        db.create()
        print("Database created")
    db_utils.add_database_name(DBType.MYSQL, db.database_name)
    
    # Sonarqube token
    server_sq = SonarqubeAPIExtended()
    sonarqube_property = sq_utils.get_sonarqube_properties()
    if sonarqube_property.token == "":
        print("Sonarqube token not found: generation of a new one")
        response = server_sq.generate_token(sonarqube_property.user, "ANITA")
        content = server_sq.get_json_content(response)
        print(content)
        sq_utils.set_token(content["token"])

    # Sonarscanner
    dirs = [f for f in os.listdir(sonarscanner_path) if os.path.isdir(join(sonarscanner_path, f))]
    if not dirs:
        print("Sonar-scanner status: not found. Sonar-scanner will be installed in a few seconds")
        zip_path = download()
        extract_content(zip_path, "sonar-scanner")
        os.remove(zip_path)
        print("\nSonar-scanner has been successfully installed")
    else:
        print("Sonar-scanner status: OK")

    return True


def resource_precondition():
    # Resource dir names
    dirs = ["software_quality", "zip", "database", "sonar-scanner"]

    # Resource direcories
    onlydirs = [f for f in os.listdir(resource_path) if os.path.isdir(join(resource_path, f))]

    folders_created = []
    for dir in dirs:
        if dir not in onlydirs:
            os.mkdir(os.path.join(resource_path, dir))
            folders_created.append(dir)

    return folders_created


