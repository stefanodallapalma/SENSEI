import sonarqube.utils.SonarqubeUtils as sq_utils
import subprocess
from sonarscanner import SonarscannerUtils as scanner_utils
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject


def run_sonarscanner(project_key, project_path):
    sq_parameters = sq_utils.get_sonarqube_properties()
    sq_local = SonarqubeLocalProject(sq_utils.get_name(project_key))

    sonar_scanner_path = scanner_utils.get_sonarscanner_path()

    # Create new tmp dir for sonarscanner process
    sq_local.create_buffer_folder()

    command = ["java", "-jar", sonar_scanner_path, "-Dsonar.sources=.", "-Dsonar.host.url=" + sq_parameters.url,
               "-Dsonar.login=" + sq_parameters.token, "-Dsonar.ce.javaOpts=-Xmx2048m"]

    # Get a list of all buffers and html files
    buffers = sq_local.get_buffers()

    for key in buffers.keys():
        sq_local.move_buffer(key)

        # Run sonar scanner
        command.append("-Dsonar.projectKey=" + project_key + "_" + key)
        process = subprocess.Popen(command, cwd=sq_local.buffer_path, shell=False, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.wait()

        sq_local.clear_buffer_folder()

    sq_local.delete_buffer_folder()

