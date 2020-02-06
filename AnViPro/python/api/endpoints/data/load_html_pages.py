from flask import request, Response, json
import os
from os.path import join
from zipfile import ZipFile
import string
import random

import utils.SonarqubePropertyUtils as sq_utils

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

        # Create the new directory
        try:
            os.mkdir(resource_folder_path)
        except OSError:
            return Response(json.dumps("Creation of the directory failed"), status=400, mimetype="application/json")

        # Generate a new project key for this project
        pk_add = False
        while pk_add is False:
            try:
                project_key = randomString()
                sq_utils.add_project(name, project_key)
                pk_add = True
            except Exception:
                pk_add = False

    # Save zip, exstract all files in the resource folder and remove zip file
    zip_file = request.files["sq_zip_html_pages"]
    zip_path = join(resource_folder_path, zip_name)
    zip_file.save(join(zip_path))

    zip = ZipFile(zip_path, "r")
    zip.extractall(resource_folder_path)
    os.remove(zip_path)

    return Response(json.dumps("Operation successsful"), status=200, mimetype="application/json")


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
