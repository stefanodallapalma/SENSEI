import datetime
import time
from os.path import join, exists

from database.anita.AnitaDB import AnitaDB
from database.anita.controller_handler import get_controller_instance
from database.db.structure.DBType import DBType
from database.utils import DBUtils as db_utils
from sonarqube.api.SonarqubeAPI import SonarqubeAPI
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.utils import SonarqubeUtils as sq_utils
from sonarscanner.SonarscannerUtils import *
from modules.trend_analysis.scraper.enum import Market
from utils.PortScanner import scanner
from utils.FileUtils import *

resource_path = "../resources/"
database_resource_path = join(resource_path, "database")
sonarscanner_path = join(resource_path, "sonar-scanner")
mysql_name = "mysql.json"
sonarqube_name = "sonarqube_properties.json"
default_name = "default.json"

LIMIT_TIME = 150     # sec


def check_preconditions():
    logger = logging.getLogger("precondition")
    logger.info("PRECONDITION CHECKING")

    # Resource folders
    folders = resource_precondition()
    if folders:
        logger.info("Resource folders: OK (" + str(folders) + " created)")
    else:
        logger.info("Resource folders: OK")

    # Parameters
    logger.info("PARAMETERS")
    # Sonarqube parameters
    sonarqube_property_path = join(resource_path, sonarqube_name)
    if not exists(sonarqube_property_path):
        logger.info("Sonarqube: parameters not found. Starting sonarqube setup")
        sonarqube_setup()
    logger.info("Sonarqube: OK")

    # MySQL parameters
    mysql_property_path = join(database_resource_path, mysql_name)
    if not exists(mysql_property_path):
        logger.info("MySQL: parameters not found. Starting mysql setup")
        mysql_setup()
    logger.info("MySQL: OK")

    # Connection test
    logger.info("CONNECTION TEST")

    # Mysql connection test
    mysql_property = db_utils.get_db_parameters(DBType.MYSQL)
    if not scanner(mysql_property.host, mysql_property.port):
        logger.info("MySQL: waiting...")
        start = int(datetime.datetime.now().timestamp())
        actual = int(datetime.datetime.now().timestamp())
        while (actual - start) < LIMIT_TIME and scanner(mysql_property.host, mysql_property.port):
            time.sleep(1)
            actual = int(datetime.datetime.now().timestamp())

        if (actual - start) >= LIMIT_TIME:
            logger.error("MySQL: server UNREACHABLE")
            return False
    logger.info("MySQL: OK")

    # Sonarqube connection test
    sonarqube_property = sq_utils.get_sonarqube_properties()
    if not scanner(sonarqube_property.host, sonarqube_property.port):
        logger.info("Sonarqube: waiting...")
        start = int(datetime.datetime.now().timestamp())
        actual = int(datetime.datetime.now().timestamp())
        while (actual - start) < LIMIT_TIME and scanner(sonarqube_property.host, sonarqube_property.port):
            time.sleep(1)
            actual = int(datetime.datetime.now().timestamp())

        if (actual - start) >= LIMIT_TIME:
            logger.error("Sonarqube: server UNREACHABLE")
            return False
    logger.info("Sonarqube: OK")

    # Wait that the server is up
    logger.info("Sonarqube status: Waiting that the server is up...")
    conn = False
    sq_api = SonarqubeAPI()
    start = int(datetime.datetime.now().timestamp())
    actual = int(datetime.datetime.now().timestamp())
    while not conn and (actual - start) < LIMIT_TIME:
        try:
            response = sq_api.server_status()
            status = SonarqubeAPI.get_json_content(response)["status"]
            if status == "UP":
                conn = True
            else:
                time.sleep(1)
        except:
            time.sleep(1)

        actual = int(datetime.datetime.now().timestamp())

    if (actual - start) >= LIMIT_TIME:
        logger.error("Sonarqube: server not ready")
        return False

    # Database
    logger.info("DATABASE")

    # MySQL schema
    db = AnitaDB(anonymous=True)
    if db.exist():
        logger.info("Schema: OK")
    else:
        logger.info("Schema: generation...")
        db.create()
        logger.info("Schema generated")
    db_utils.add_database_name(DBType.MYSQL, db.database_name)

    # MySQL tables
    tables = ["sonarqube", "product", "vendor", "feedback"]
    for table in tables:
        controller = get_controller_instance(table)
        if controller.exist():
            logger.info(table.upper() + " table: OK")
        else:
            logger.info(table.upper() + " table: generation...")
            result = controller.create(encode="utf8mb4")
            if not result:
                logger.info(result)
                return False
            logger.info(table.upper() + " table generated")

    # Sonarqube token
    server_sq = SonarqubeAPIExtended()
    sonarqube_property = sq_utils.get_sonarqube_properties()
    if sonarqube_property.token == "":
        response = server_sq.search_tokens(sonarqube_property.user)
        search_content = server_sq.get_json_content(response)
        if "userTokens" in search_content and len(search_content["userTokens"]) > 0:
            for user_token in search_content["userTokens"]:
                if user_token["name"] == "ANITA":
                    server_sq.revoke_token(sonarqube_property.user, "ANITA")
                    logger.info("Sonarqube: old token revoked")

        logger.info("Sonarqube: generation of a new token")
        response = server_sq.generate_token(sonarqube_property.user, "ANITA")
        content = server_sq.get_json_content(response)
        sq_utils.set_token(content["token"])

    # Sonarscanner
    dirs = [f for f in os.listdir(sonarscanner_path) if os.path.isdir(join(sonarscanner_path, f))]
    if not dirs:
        logger.info("Sonar-scanner status: not found. Sonar-scanner will be installed in a few seconds")
        zip_path = download()
        extract_content(zip_path, "sonar-scanner")
        os.remove(zip_path)
        logger.info("Sonar-scanner has been successfully installed")
    else:
        logger.info("Sonar-scanner status: OK")

    return True


def resource_precondition():
    # Resource dir names
    dirs = ["software_quality", "trend_analysis", "zip", "database", "sonar-scanner"]

    # Resource directories
    onlydirs = [f for f in os.listdir(resource_path) if os.path.isdir(join(resource_path, f))]

    folders_created = []
    for dir in dirs:
        if dir not in onlydirs:
            os.mkdir(os.path.join(resource_path, dir))
            folders_created.append(dir)

            if dir == "trend_analysis":
                ta_path = os.path.join(resource_path, dir)
                markets_path = os.path.join(ta_path, "markets")
                os.mkdir(markets_path)

                market_list = [market.name.lower() for market in Market if market.value != 0]
                for market in market_list:
                    os.mkdir(os.path.join(markets_path, market))

    return folders_created


def mysql_setup():
    default_dict = load_json(join(resource_path, default_name))
    host = default_dict["mysql_host"]
    if "https" in host:
        host = host.replace("https://", "")
    elif "http" in host:
        host = host.replace("http://", "")

    port = default_dict["mysql_port"]
    user = default_dict["mysql_user"]
    password = default_dict["mysql_password"]

    mysql_dict = {"host": host, "port": port, "user": user, "password": password, "database_name": ""}

    output_path = join(database_resource_path, "mysql.json")
    save_json(output_path, mysql_dict)


def sonarqube_setup():
    default_dict = load_json(join(resource_path, default_name))
    host = default_dict["sonarqube_host"]
    port = default_dict["sonarqube_port"]
    user = default_dict["sonarqube_user"]
    password = default_dict["sonarqube_password"]

    sonarqube_dict = {"host": host, "port": port, "user": user, "password": password, "token": "", "projects": []}

    output_path = join(resource_path, sonarqube_name)
    save_json(output_path, sonarqube_dict)


def sonarscanner_setup():
    zip_path = download()
    extract_content(zip_path, "sonar-scanner")
    os.remove(zip_path)
