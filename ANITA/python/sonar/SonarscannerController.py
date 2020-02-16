import utils.SonarqubeUtils as sq_utils
import shutil
import os
import subprocess
import json
from os.path import isfile, join
from utils.ListUtils import array_split

scannerwork_folder_name = ".scannerwork"
jsonbuffer_name = "infoBuffer.json"

def run_sonarscanner(project_key, project_path):
    sonarqubeParameters = sq_utils.get_sonarqube_properties()

    command = []
    command.append("sonar-scanner")
    command.append("-Dsonar.sources=.")
    command.append("-Dsonar.host.url=" + sonarqubeParameters.url)
    command.append("-Dsonar.login=" + sonarqubeParameters.token)
    command.append("-Dsonar.ce.javaOpts=-Xmx2048m")

    project = sq_utils.get_project("Key", project_key)

    # Create new tmp dir for sonarscanner process
    tmp_path = project_path + os.path.sep + "tmp"
    os.mkdir(tmp_path)

    # Get a list of all buffers and html files
    json_path = project_path + os.path.sep + project["Name"] + "_" + jsonbuffer_name
    with open(json_path) as json_file:
        json_buffer = json.loads(json_file.read())

    for i in range(len(json_buffer)):
        buffer = json_buffer[str(i+1)]
        print(str(buffer))

        # Copy all buffer's files into tmp dir
        for file in buffer:
            file_path = project_path + os.path.sep + file
            new_file_path = tmp_path + os.path.sep + file
            shutil.copy(file_path, new_file_path)

        # Run sonar scanner
        command.append("-Dsonar.projectKey=" + project_key + "_" + str(i+1))
        process = subprocess.Popen(command, cwd=tmp_path)
        process.wait()

        # Delete all buffer's files into tmp dir
        for file in buffer:
            file_path = tmp_path + os.path.sep + file
            os.remove(file_path)

    # Delete tmp folder
    shutil.rmtree(tmp_path)

