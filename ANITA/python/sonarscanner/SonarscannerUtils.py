import requests
import os, sys, logging
from sys import platform
from zipfile import ZipFile

sonarscanner_path = "../resources/sonar-scanner/"
sonarscanner_filename = "sonarscanner.zip"

linux_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip"
windows_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-windows.zip"
mac_download_path = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-macosx.zip"

logger = logging.getLogger("sonarscanner")


def download():
    output_dirs = [f for f in os.listdir(sonarscanner_path) if os.path.isdir(os.path.join(sonarscanner_path, f))]
    if output_dirs:
        raise Exception("Sonarscanner already installed")

    # Download sonarscanner
    if platform == "linux" or platform == "linux2":
        link = linux_download_path
    elif platform == "darwin":
        link = mac_download_path
    else:
        link = windows_download_path

    sonarscanner_zip_path = os.path.join(sonarscanner_path, sonarscanner_filename)
    with open(sonarscanner_zip_path, "wb") as f:
        print("Downloading %s" % sonarscanner_filename)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

    return sonarscanner_zip_path


def extract_content(zip_path, name_folder=None):
    # Extract zip
    zip = ZipFile(zip_path, "r")
    zip.extractall(sonarscanner_path)

    output_dirs = [f for f in os.listdir(sonarscanner_path) if os.path.isdir(os.path.join(sonarscanner_path, f))]
    if not output_dirs:
        raise Exception("Problem with zip extraction")

    if name_folder is not None:
        prev_path = os.path.join(sonarscanner_path, output_dirs[0])
        actual_path = os.path.join(sonarscanner_path, name_folder)
        os.rename(prev_path, actual_path)


def get_sonarscanner_path():
    dirs = [f for f in os.listdir(sonarscanner_path) if os.path.isdir(os.path.join(sonarscanner_path, f))]
    path = os.path.join(sonarscanner_path, dirs[0])
    path = os.path.join(path, "lib")

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    path = os.path.join(path, files[0])

    return os.path.abspath(path)
