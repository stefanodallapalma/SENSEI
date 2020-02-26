from flask import request, Response, json
import sonarqube.utils.SonarqubeUtils as sq_utils
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from sonarscanner.SonarscannerController import run_sonarscanner as scanner
from database.anita.table.SonarqubeTable import SonarqubeTable
from database.anita.controller.SonarqubeController import get_beans


# Endpoint
def load_new_data():
    # Load parameters
    name = request.form["resource_folder_name"]
    zip_file = request.files["sq_zip_html_pages"]

    # Parameter
    local_sq = SonarqubeLocalProject(name)
    server_sq = SonarqubeAPIExtended()
    anita_sq_api = SonarqubeAnitaAPI()
    project_key = sq_utils.generate_project_key()

    print("Check precondition")
    # Preconditions
    if local_sq.exist():
        return Response(json.dumps("The project already exists"), status=400, mimetype="application/json")

    print("Create local project")
    # Local
    create_project = local_sq.create_project()
    if not create_project:
        return Response(json.dumps("Creation of the project failed: impossible to create the folder (OSError)"), status=400, mimetype="application/json")

    local_sq.save_and_extract(zip_file)
    local_sq.add_buffer_info()

    # Sonarqube json info
    raw_files = local_sq.get_raw_files()
    sq_utils.add_project(name, project_key, len(raw_files), local_sq.BUFFER_SIZE)

    print("Create project on sonarqube")
    # Sonarqube server
    create_response = server_sq.create_project(name, project_key)

    if 400 <= create_response.status_code < 500:
        return Response(json.dumps(create_response.json()), status=create_response.status_code, mimetype="application/json")

    # Sonar scanner
    print("Waiting for sonarscanner...")
    scanner(project_key, local_sq.project_path)
    print("Sonarscanner has been executed successfully")

    # Retrieve metrics
    print("Waiting for pending tasks...")
    measures = anita_sq_api.measures(project_key, wait=True)
    print("Metrics retrieved")

    print("Save info on db")
    # Sonarqube Database
    sq_table = SonarqubeTable()
    if not sq_table.exist():
        sq_table.create()

    sq_beans = get_beans(name, measures)
    sq_table.insert_values(sq_beans)

    local_sq.delete_raw()

    return Response(json.dumps("Operation successful"), status=200, mimetype="application/json")
