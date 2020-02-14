from flask import request, Response, json
import os
from os.path import join, isfile
from zipfile import ZipFile
import string
import random
import utils.SonarqubeUtils as sq_utils
import sonar.SonarqubeAPIController as sq_api_controller
from sonar.SonarscannerController import run_sonarscanner as scanner

from exception import DuplicateProjectNameException, DuplicateProjectKeyException
from exception.NoProjectException import NoProjectException

html_pages_path = "../resources/html_pages/"
zip_name = "tmpZip.zip"
scannerwork_folder_name = ".scannerwork"

MAX_PROJECT_SIZE = 100


def load_new_data():
    project_key = None

    name = request.form["resource_folder_name"]

    # Check if the resource folder name is available or not
    try:
        project = sq_utils.get_project("Name", name)
        return Response(json.dumps("The resource folder already exists"), status=400, mimetype="application/json")
    except NoProjectException:
        pass

    resource_folder_path = join(html_pages_path, name)

    # Create the new directory
    try:
        os.mkdir(resource_folder_path)
    except OSError:
        return Response(json.dumps("Creation of the directory failed"), status=400, mimetype="application/json")

    # Save zip, exstract all files in the resource folder and remove zip file
    zip_file = request.files["sq_zip_html_pages"]
    zip_path = join(resource_folder_path, zip_name)
    zip_file.save(join(zip_path))

    zip = ZipFile(zip_path, "r")
    zip.extractall(resource_folder_path)
    os.remove(zip_path)

    # Number of files loaded
    onlyfiles = [f for f in os.listdir(resource_folder_path) if isfile(join(resource_folder_path, f))]
    count = len(onlyfiles)

    # Generate a new project key for this project
    while project_key is None:
        try:
            key_length = random.randint(10, 51)
            project_key = randomString(key_length)
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

    return Response(json.dumps("Operation successful"), status=200, mimetype="application/json")


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
