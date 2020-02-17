import requests
from io import StringIO
import os
from sys import platform
import subprocess
from zipfile import ZipFile

from exception.NoJDKFoundException import NoJDKFoundException

linux_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip"
windows_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-windows.zip"
mac_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-macosx.zip"

sonarscanner_filename = "sonarscanner.zip"


def setup(output_dir, name_folder):
    output_dirs = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]
    if output_dirs:
        raise Exception("Folder not empty")

    # Download sonarscanner
    if platform == "linux" or platform == "linux2":
        link = linux_download_path
    elif platform == "darwin":
        link = mac_download_path
    elif platform == "win32":
        link = windows_download_path

    # TO DO
    if not check_precondition():
        raise NoJDKFoundException()

    sonarscanner_zip_path = output_dir + sonarscanner_filename
    response = requests.get(link, stream=True)
    open(sonarscanner_zip_path, "wb").write(response.content)

    # Extract zip
    zip = ZipFile(sonarscanner_zip_path, "r")
    zip.extractall(output_dir)
    os.remove(sonarscanner_zip_path)

    output_dirs = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]
    if not output_dirs:
        raise Exception("Problem with zip extraction")

    prev_path = os.path.join(output_dir, output_dirs[0])
    actual_path = os.path.join(output_dir, name_folder)
    os.rename(prev_path, actual_path)


def check_precondition():
    # Check if JVM is installed
    try:
        process = subprocess.run(["java", "--version"])
        return True
    except FileNotFoundError:
        return False