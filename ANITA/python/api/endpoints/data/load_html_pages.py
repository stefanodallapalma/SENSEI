import os, string, random
from flask import request, Response, json
from os.path import join, isfile
from zipfile import ZipFile
from services.quality.metrics import retrieve_metrics
from utils.FileUtils import getfiles
from utils.ListUtils import array_split
import utils.SonarqubeUtils as sq_utils
import sonar.SonarqubeAPIController as sq_api_controller
from sonar.SonarscannerController import run_sonarscanner as scanner
from database.anita.quality.QualityTable import QualityTable

from exception import DuplicateProjectNameException, DuplicateProjectKeyException

html_pages_path = "../resources/html_pages/"
zip_name = "tmpZip.zip"
scannerwork_folder_name = ".scannerwork"
jsonbuffer_suffix = "infoBuffer.json"

MAX_PROJECT_SIZE = 100


# Endpoint
def load_new_data():
    project_key = None
    name = request.form["resource_folder_name"]
    resource_folder_path = join(html_pages_path, name)

    # Check if the resource folder name is available or not
    if os.path.exists(resource_folder_path):
        return Response(json.dumps("The resource folder already exists"), status=400, mimetype="application/json")

    # Create the new directory
    try:
        os.mkdir(resource_folder_path)
    except OSError:
        return Response(json.dumps("Creation of the directory failed"), status=400, mimetype="application/json")

    # Save zip, exstract all files in the resource folder and remove zip file
    zip_path = join(resource_folder_path, zip_name)
    zip_file = request.files["sq_zip_html_pages"]
    zip_file.save(join(zip_path))
    zip = ZipFile(zip_path, "r")
    zip.extractall(resource_folder_path)
    os.remove(zip_path)

    # Number of files loaded
    onlyfiles = getfiles(resource_folder_path)
    count = len(onlyfiles)

    # Create the json with the information of each subproject
    jsonbuffer_name = name + "_" + jsonbuffer_suffix
    output_infojson = join(resource_folder_path, jsonbuffer_name)
    add_json_buffer(onlyfiles, output_infojson, MAX_PROJECT_SIZE)

    # Generate a new project key for this project
    while project_key is None:
        try:
            key_length = random.randint(10, 51)
            project_key = random_string(key_length)
        except DuplicateProjectNameException:
            project_key = None
        except DuplicateProjectKeyException:
            project_key = None

    # Add the info of the project into the sonarqube json
    sq_utils.add_project(name, project_key, count, MAX_PROJECT_SIZE)

    # Create the project on sonarqube
    create_response = sq_api_controller.create_project(name, project_key)

    if 400 <= create_response.status_code < 500:
        return Response(json.dumps(create_response.json()), status=create_response.status_code, mimetype="application/json")

    # Run sonar scanner to load html pages on sonarqube
    source = html_pages_path + name
    scanner(project_key, source)

    # Retrieve metrics
    qualities = retrieve_metrics(project_key)

    # Save quality metrics into db
    metric_list = sq_api_controller.metric_list()

    # Create the table, if it does not exist
    quality_table = QualityTable()
    if not quality_table.exist():
        quality_table.create_quality_table(metric_list)

    quality_table.insert_qualities(metric_list, qualities)

    

    return Response(json.dumps("Operation successful"), status=200, mimetype="application/json")


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def add_json_buffer(files, output_file, buffer_size):
    json_buffer = {}
    buffers = array_split(files, buffer_size)

    i = 1
    for buffer in buffers:
        json_buffer[i] = buffer
        i += 1

    with open(output_file, 'w') as outfile:
        json.dump(json_buffer, outfile)