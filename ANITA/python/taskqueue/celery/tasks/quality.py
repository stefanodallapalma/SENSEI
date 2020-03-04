from __future__ import absolute_import

# Standard library imports
import time

# Third party imports
from celery import states

# Local application imports
from taskqueue.celery.config import celery
import sonarqube.utils.SonarqubeUtils as sq_utils
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from sonarscanner.SonarscannerController import run_sonarscanner as scanner
from database.anita.table.SonarqubeTable import SonarqubeTable
from database.anita.controller.SonarqubeController import get_beans

LOAD_PAGE_TASK_ID = "1"


@celery.task(bind=True)
def sample(self):
    test_time = 20

    test_time_1 = 5
    test_time_2 = 10
    test_time_3 = 15

    test_dict = {"Test 1": 0.0, "Test 2": 0.0, "Test 3": 0.0, "Test 4": 0.0, }

    self.update_state(state=states.STARTED, meta=test_dict)

    start_time = time.time()
    actual_time = time.time()

    while actual_time - start_time < test_time:
        if actual_time - start_time < test_time_1:
            test_dict["Test 1"] = (actual_time - start_time) / test_time_1
        elif actual_time - start_time < test_time_2:
            test_dict["Test 1"] = 1.0
            test_dict["Test 2"] = (actual_time - start_time) / test_time_2
        elif actual_time - start_time < test_time_3:
            test_dict["Test 2"] = 1.0
            test_dict["Test 3"] = (actual_time - start_time) / test_time_3
        else:
            test_dict["Test 3"] = 1.0
            test_dict["Test 4"] = (actual_time - start_time) / test_time

        self.update_state(state='PROGRESS', meta=test_dict)
        time.sleep(1)

        actual_time = time.time()

    test_dict["Test 4"] = 1.0

    self.update_state(state=states.SUCCESS, meta=test_dict)
    return test_dict


@celery.task(bind=True)
def load_pages(self, project_name):
    # Response content
    content = load_pages_content_template()
    self.update_state(state=states.STARTED, meta=content)

    # Parameter
    local_sq = SonarqubeLocalProject(project_name)
    server_sq = SonarqubeAPIExtended()
    anita_sq_api = SonarqubeAnitaAPI()
    project_key = sq_utils.generate_project_key()

    # STEP 2 - SONARQUBE PROJECT - SETUP
    raw_files = local_sq.get_raw_files()
    sq_utils.add_project(project_name, project_key, len(raw_files), local_sq.BUFFER_SIZE)

    create_response = server_sq.create_project(project_name, project_key)

    if 400 <= create_response.status_code < 500:
        content["msg"] = create_response.json()
        self.update_state(state=states.FAILURE, meta=content)
        return content

    content["steps"]["Sonarqube project - Setup"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 3 - SONARQUBE PROJECT - SENDING PAGES
    scanner(project_key, local_sq.project_path)
    content["steps"]["Sonarqube project - Sending pages"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 4 - SONARQUBE PROJECT - PROCESSING
    measures = anita_sq_api.measures(project_key, wait=True)
    content["steps"]["Sonarqube project - Processing"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 5 - SAVE DATA ON DB
    sq_table = SonarqubeTable()
    if not sq_table.exist():
        sq_table.create()

    sq_beans = get_beans(project_name, measures)
    sq_table.insert_values(sq_beans)

    content["steps"]["Save data on db"] = True
    self.update_state(state='PROGRESS', meta=content)

    # Clear local raw files
    local_sq.delete_raw()

    # STEP 6 - SONARQUBE PROJECT - DELETE PROJECT
    sq_utils.delete_project(project_name)
    remove_response = server_sq.delete_project(project_key)
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
