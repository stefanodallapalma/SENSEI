from flask import request, Response, json
import wget
from sys import platform
import subprocess

download_path = "../resources/download/"

linux_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip"
windows_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-windows.zip"
mac_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-macosx.zip"

sonarscanner_filename = "sonarscanner.zip"

def setup():
    # Download sonarscanner
    if platform == "linux" or platform == "linux2":
        link = linux_download_path
    elif platform == "darwin":
        link = mac_download_path
    elif platform == "win32":
        link = windows_download_path
    print(link)

    # TO DO
    if check_precondition():
        pass

    #sonarscanner_zip_path = download_path + sonarscanner_filename
    #sonarscanner_zip = wget.download(link, out=sonarscanner_zip_path)

def check_precondition():
    # Check if JVM is installed
    try:
        process = subprocess.run(["java", "--version"])
        return True
    except FileNotFoundError:
        return False