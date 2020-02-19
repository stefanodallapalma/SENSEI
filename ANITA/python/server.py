import os, sys, connexion
from flask_cors import CORS
from utils import SonarqubeUtils as sq_utils
from utils import SonarscannerUtils as scanner_utils
from utils.PortScanner import scanner
from sonar import SonarqubeAPIController as sq_api_controller


# Sonarscanner path
scanner_path = "../../Sonar-scanner/"

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger/conf.yml")
app.add_api("swagger/data.yml")
app.add_api('swagger/swagger.yml')
app.add_api('swagger/resources.yml')
app.add_api("swagger/softwarequality.yml")


def resource_preconditions():
    # Resource path and dir names
    resource_path = "../resources/"
    dirs = ["html_pages", "zip"]

    # Resource direcories
    onlydirs = [f for f in os.listdir(resource_path) if os.path.isdir(os.path.join(resource_path, f))]

    folders_created = []
    for dir in dirs:
        if dir not in onlydirs:
            os.mkdir(os.path.join(resource_path, dir))
            folders_created.append(dir)

    return folders_created


def sonarqube_precondition():
    sq_param = sq_utils.get_sonarqube_properties()

    status = scanner(sq_param.host, sq_param.port)
    if not status:
        print("Sonarqube is not reachable")
    else:
        # Sonarqube token
        sq_param = sq_utils.get_sonarqube_properties()
        if sq_param.token == "":
            print("TOKEN NOT FOUND: Generation of a new token")
            response = sq_api_controller.generate_token(sq_param.user, "ANITA")
            content = sq_api_controller.get_content(response)
            sq_utils.set_token(content["token"])

    return status


def mysql_precondition():
    host = "127.0.0.1"
    port = 3306

    status = scanner(host, port)
    if not status:
        print("MySQL is not reachable")

    return status


def check_preconditions():
    print("PRECONDITION")
    # Resource
    print("Resource folders")
    folders_created = resource_preconditions()
    if not folders_created:
        print("No folders created")
    else:
        print("Folders created:")
        for folder in folders_created:
            print("\t- " + folder)

    # Mysql
    print("MySQL")
    status = mysql_precondition()
    if not status:
        return False

    # Sonarqube
    print("Sonarqube")
    status = sonarqube_precondition()
    if not status:
        return False

    # Sonarscanner
    onlydirs = [f for f in os.listdir(scanner_path) if os.path.isdir(os.path.join(scanner_path, f))]
    if "sonar-scanner" not in onlydirs:
        scanner_utils.setup(scanner_path, "sonar-scanner")

    return True


def setup():
    print("MySQL setup")
    if mysql_precondition():
        print("MySQL has already been setup")
    else:
        # TO DO
        pass
    print("\n")

    print("Sonarqube network setup")
    if sonarqube_precondition():
        print("MySQL has already been setup")
    print("Sonar-scanner setup")

    pass


if __name__ == "__main__":
    """if len(sys.argv) > 1:
        raise Exception("Too many arguments")

    # First setup
    if sys.argv:
        if sys.argv[0] == "-fs":
            setup()
        elif sys.argv[0] == "-h":
            print("\t-fs\t\tRun the server in the first setup mode")
            sys.exit()

    result = check_preconditions()"""

    app.run(host='0.0.0.0', port=5000, debug=True)


