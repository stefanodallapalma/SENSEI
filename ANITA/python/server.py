import os
from utils import SonarqubeUtils as sq_utils
from utils import SonarscannerUtils as scanner_utils
from sonar import SonarqubeAPIController as sq_api_controller
import connexion
from flask_cors import CORS

# Resource path and dir names
resource_path = "../resources/"
dirs = ["html_pages", "zip"]

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


def check_preconditions():
    # Resource direcories
    onlydirs = [f for f in os.listdir(resource_path) if os.path.isdir(os.path.join(resource_path, f))]

    for dir in dirs:
        if dir not in onlydirs:
            os.mkdir(os.path.join(resource_path, dir))

    # Sonarqube token
    sq_param = sq_utils.get_sonarqube_properties()
    if sq_param.token == "":
        response = sq_api_controller.generate_token(sq_param.user, "ANITA")
        content = sq_api_controller.get_content(response)
        sq_utils.set_token(content["token"])

    # Sonarscanner
    onlydirs = [f for f in os.listdir(scanner_path) if os.path.isdir(os.path.join(scanner_path, f))]
    if "sonar-scanner" not in onlydirs:
        scanner_utils.setup(scanner_path, "sonar-scanner")


if __name__ == "__main__":
    check_preconditions()
    app.run(host='0.0.0.0', port=5000, debug=True)

