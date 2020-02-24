from flask import request, Response, json
from sonarqube.metrics import retrieve_metrics
import sonarqube.utils.SonarqubeUtils as sq_utils
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from sonarscanner.SonarscannerController import run_sonarscanner as scanner
from database.anita.sonarqube.SonarqubeTable import QualityTable


# Endpoint
def load_new_data():
    # Load parameters
    name = request.form["resource_folder_name"]
    zip_file = request.files["sq_zip_html_pages"]

    # Parameter
    local_sq = SonarqubeLocalProject(name)
    server_sq = SonarqubeAPIExtended()
    project_key = sq_utils.generate_project_key()

    # Preconditions
    if local_sq.exist():
        return Response(json.dumps("The project already exists"), status=400, mimetype="application/json")

    # Local
    create_project = local_sq.create_project()
    if not create_project:
        return Response(json.dumps("Creation of the project failed: impossible to create the folder (OSError)"), status=400, mimetype="application/json")

    local_sq.save_and_extract(zip_file)
    local_sq.add_buffer_info()

    # Sonarqube json info
    raw_files = local_sq.get_raw_files()
    sq_utils.add_project(name, project_key, len(raw_files), local_sq.BUFFER_SIZE)

    # Sonarqube server
    create_response = server_sq.create_project(name, project_key)

    if 400 <= create_response.status_code < 500:
        return Response(json.dumps(create_response.json()), status=create_response.status_code, mimetype="application/json")

    # Sonar scanner
    scanner(project_key, local_sq.project_path)

    # Retrieve metrics
    qualities = retrieve_metrics(project_key, wait=True)

    # Sonarqube Database
    response_metric = server_sq.metric_list()
    metric_list = server_sq.get_json_content(response_metric)

    # Create the table, if it does not exist
    quality_table = QualityTable()
    if not quality_table.exist():
        quality_table.create_quality_table(metric_list)

    quality_table.insert_qualities(metric_list, qualities)

    local_sq.delete_raw()

    return Response(json.dumps("Operation successful"), status=200, mimetype="application/json")
