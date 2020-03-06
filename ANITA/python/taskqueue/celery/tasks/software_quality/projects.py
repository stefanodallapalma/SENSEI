from __future__ import absolute_import

# Standard library imports
import time, json
from datetime import datetime

# Third party imports
from celery import states

# Local application imports
from taskqueue.celery.config import celery
import sonarqube.utils.SonarqubeUtils as sq_utils
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from sonarscanner.SonarscannerController import run_sonarscanner as scanner
from database.anita.controller.SonarqubeController import SonarqubeController
from database.anita.decoder.sonarqube_decoder import SonarqubeServerDecoder

# Task ID
LOAD_PAGE_TASK_ID = "1"


@celery.task(bind=True)
def load_pages(self, project_name, known_project_name):
    # Response content
    content = load_pages_content_template()
    self.update_state(state=states.STARTED, meta=content)

    # Parameter
    sq_local = SonarqubeLocalProject(project_name)
    sq_server = SonarqubeAPIExtended()
    sq_api_anita = SonarqubeAnitaAPI()
    project_key = sq_utils.generate_project_key()

    # STEP 2 - SONARQUBE PROJECT - SETUP
    raw_files = sq_local.get_raw_files()
    sq_utils.add_project(project_name, project_key, len(raw_files), sq_local.BUFFER_SIZE)

    create_response = sq_server.create_project(project_name, project_key)

    if 400 <= create_response.status_code < 500:
        content["msg"] = create_response.json()
        self.update_state(state=states.FAILURE, meta=content)
        return content

    content["steps"]["Sonarqube project - Setup"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 3 - SONARQUBE PROJECT - SENDING PAGES
    scanner(project_key, sq_local.project_path)
    content["steps"]["Sonarqube project - Sending pages"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 4 - SONARQUBE PROJECT - PROCESSING
    measures = sq_api_anita.measures(project_key, wait=True)
    content["steps"]["Sonarqube project - Processing"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 5 - SAVE DATA ON DB
    sq_controller = SonarqubeController()
    if not sq_controller.exist():
        sq_controller.create()

    timestamp = int(datetime.now().timestamp())
    bean_dict = {"project_name": project_name, "timestamp": timestamp, "pages": measures}
    sq_beans = json.loads(bean_dict, cls=SonarqubeServerDecoder)
    sq_controller.insert_beans(sq_beans)

    content["steps"]["Save data on db"] = True
    self.update_state(state='PROGRESS', meta=content)

    # Clear local raw files
    sq_local.delete_raw()

    # STEP 6 - SONARQUBE PROJECT - DELETE PROJECT
    sq_utils.delete_project(project_name)
    remove_response = sq_server.delete_project(project_key)
    if remove_response.status_code >= 400:
        content["msg"] = "Impossible to delete project on sonarqube"
        self.update_state(state=states.FAILURE, meta=content)
        return content

    content["steps"]["Sonarqube project - Delete project"] = True
    self.update_state(state=states.SUCCESS, meta=content)
    return content


def load_pages_content_template():
    steps = {"Save data": True, "Sonarqube project - Setup": False, "Sonarqube project - Sending pages": False,
             "Sonarqube project - Processing": False, "Save data on db": False,
             "Sonarqube project - Delete project": False}

    content = {"steps": steps, "msg": ""}
    return content
