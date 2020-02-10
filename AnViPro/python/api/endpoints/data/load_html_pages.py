from flask import request, Response, json
import os
from os.path import join
from zipfile import ZipFile
import string
import random
import subprocess
from sonar.bean.SonarqubeParameters import SonarqubeParameters
import utils.SonarqubeUtils as sq_utils
import sonar.SonarqubeAPI as sqAPI

from exception import DuplicateProjectNameException, DuplicateProjectKeyException

html_pages_path = "../resources/html_pages/"
zip_name = "tmpZip.zip"


def load_data():
    if "sq_zip_html_pages" not in request.files:
        return Response(json.dumps("No zip file passed as parameter"), status=400, mimetype="application/json")

    if "resource_folder_name" not in request.form and "resource_folders_list" not in request.form:
        return Response(json.dumps("No resource folder name file passed as parameter"), status=400,
                        mimetype="application/json")

    new_folder = False
    if "resource_folders_list" not in request.form:
        new_folder = True
        name = request.form["resource_folder_name"]
    else:
        name = request.form["resource_folders_list"]

    resource_folder_path = join(html_pages_path, name)

    if new_folder:
        # Check if the resource folder name is available or not
        if os.path.exists(resource_folder_path):
            return Response(json.dumps("The resource folder alreasy exists"), status=400, mimetype="application/json")

        # Generate a new project key for this project
        project_key = None
        while project_key is None:
            try:
                key_length = random.randint(10, 51)
                project_key = randomString(key_length)

                # Add the project key into the sonarqube json
                sq_utils.add_project(name, project_key)
            except DuplicateProjectNameException:
                project_key = None
            except DuplicateProjectKeyException:
                project_key = None

        # Create the project on sonarqube
        create_response = sqAPI.create_project(name, project_key)
        if 400 <= create_response.status_code < 500:
            return Response(json.dumps(create_response.json()), status=create_response.status_code, mimetype="application/json")

        # If the creation of the sonarqube project succeed, then create the environment for received data on the server
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

    # Run sonar scanner to load html pages on sonarqube
    sonarqubeParameters = sq_utils.get_sonarqube_properties()

    # Sonar scanner parameter
    token = sonarqubeParameters.token
    project_key = sq_utils.get_project_key(name)
    source = html_pages_path + name

    if project_key is None:
        return Response(json.dumps("No Project key found for the current project"), status=400, mimetype="application/json")

    #subprocess.run("sonar-scanner", "-Dsonar.projectKey=" + project_key, "-Dsonar.sources=" + source,
    #               "-Dsonar.host.url=" + sonarqubeParameters.url, "-Dsonar.login=" + sonarqubeParameters.token)

    return Response(json.dumps("Operation successful"), status=200, mimetype="application/json")


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
