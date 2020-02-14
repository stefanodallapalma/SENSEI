import utils.SonarqubeUtils as sq_utils
import shutil
import os
import subprocess
from os.path import isfile, join
from utils.ListUtils import array_split

scannerwork_folder_name = ".scannerwork"

def run_sonarscanner(project_key, project_path):
    sonarqubeParameters = sq_utils.get_sonarqube_properties()

    command = []
    command.append("sonar-scanner")
    command.append("-Dsonar.sources=.")
    command.append("-Dsonar.host.url=" + sonarqubeParameters.url)
    command.append("-Dsonar.login=" + sonarqubeParameters.token)
    command.append("-Dsonar.ce.javaOpts=-Xmx2048m")

    project = sq_utils.get_project("Key", project_key)
    buffer_size = project["ProjectSize"]

    # Create new tmp dir for sonarscanner process
    tmp_path = project_path + os.path.sep + "tmp"
    os.mkdir(tmp_path)

    # Get a list of all files in the project directory
    onlyfiles = [f for f in os.listdir(project_path) if isfile(join(project_path, f))]
    buffers = array_split(onlyfiles, buffer_size)

    i = 1
    for buffer in buffers:
        # Copy all buffer's files into tmp dir
        for file in buffer:
            file_path = project_path + os.path.sep + file
            new_file_path = tmp_path + os.path.sep + file
            shutil.copy(file_path, new_file_path)

        # Run sonar scanner
        command.append("-Dsonar.projectKey=" + project_key + "_" + str(i))
        process = subprocess.Popen(command, cwd=tmp_path)
        process.wait()

        # Delete all buffer's files into tmp dir
        for file in buffer:
            file_path = tmp_path + os.path.sep + file
            os.remove(file_path)

        i += 1

    # Delete tmp folder
    shutil.rmtree(tmp_path)

