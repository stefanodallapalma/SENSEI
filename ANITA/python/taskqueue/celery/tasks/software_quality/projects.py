from __future__ import absolute_import

# Standard library imports
import json

# Third party imports
from celery import states

# Local application imports
from modules.software_quality.projects.combining_data import extra_features
from taskqueue.celery.config import celery
import sonarqube.utils.SonarqubeUtils as sq_utils
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from sonarscanner.SonarscannerController import run_sonarscanner as scanner
from database.anita.controller.SonarqubeController import SonarqubeController
from database.anita.decoder.sonarqube_decoder import *
from exception.PendingTaskException import PendingTaskException

# Task ID
LOAD_PAGE_TASK_ID = "1"
REVERSE_LOAD_PAGE_TASK_ID = "2"


@celery.task(bind=True)
def load_pages(self, project_name, timestamp, additional_info):
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
        content["error"] = create_response.json()
        self.update_state(state=states.FAILURE, meta=content)
        return content

    content["steps"]["2 - Sonarqube project - Setup"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 3 - SONARQUBE PROJECT - SENDING PAGES
    scanner(project_key, sq_local.project_path)
    content["steps"]["3 - Sonarqube project - Sending pages"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 4 - SONARQUBE PROJECT - PROCESSING
    try:
        measures = sq_api_anita.measures(project_key, wait=True)
        content["steps"]["4 - Sonarqube project - Processing"] = True
        self.update_state(state='PROGRESS', meta=content)
    except PendingTaskException as pte:
        content["error"] = "PendingTaskException"
        content["msg"] = str(pte)
        self.update_state(states.FAILURE, meta=content)
        return content

    # STEP 5 - SAVE DATA ON DB
    sq_controller = SonarqubeController()
    try:
        create_status = sq_controller.exist()
        if not create_status:
            sq_controller.create()
    except Exception as e:
        content["error"] = "Impossible to create the table into the db"
        content["msg"] = str(e)
        self.update_state(states.FAILURE, meta=content)
        return content

    bean_dict = json.dumps({"project_name": project_name, "timestamp": timestamp, "pages": measures})
    sq_beans = json.loads(bean_dict, cls=SonarqubeServerDecoder)

    try:
        sq_controller.insert_beans(sq_beans)
    except Exception as e:
        content["error"] = "Impossible to insert beans into the db"
        content["msg"] = str(e)
        self.update_state(states.FAILURE, meta=content)
        return content

    content["steps"]["5 - Save data on db"] = True
    self.update_state(state='PROGRESS', meta=content)

    # STEP 6 - ADDITIONAL INFO
    if additional_info:
        try:
            add_dicts = extra_features(project_name)
            add_beans = []
            for add_dict in add_dicts:
                add_dict["timestamp"] = str(timestamp)
                add_json = json.dumps(add_dict)
                add_bean = json.loads(add_json, cls=SonarqubeAdditionalInfoDecoder)
                add_beans.append(add_bean)

            sq_controller.update_beans(add_beans)
        except Exception as e:
            content["error"] = "Impossible to insert further informations"
            content["msg"] = str(e)
            self.update_state(states.FAILURE, meta=content)
            return content

    content["steps"]["6 - Additional Info"] = True
    self.update_state(state='PROGRESS', meta=content)

    # Clear local raw files
    sq_local.delete_raw()

    # STEP 7 - SONARQUBE PROJECT - DELETE PROJECT
    remove_response = sq_server.delete_project(project_key)
    if remove_response.status_code >= 400:
        content["error"] = "Impossible to delete project on sonarqube"
        self.update_state(state=states.FAILURE, meta=content)
        return content

    sq_utils.delete_project(project_name)

    content["steps"]["7 - Sonarqube project - Delete project"] = True
    self.update_state(state=states.SUCCESS, meta=content)

    return content


def load_pages_content_template():
    steps = {"1 - Save data": True, "2 - Sonarqube project - Setup": False, "3 - Sonarqube project - Sending pages": False,
             "4 - Sonarqube project - Processing": False, "5 - Save data on db": False,
             "6 - Additional Info": False, "7 - Sonarqube project - Delete project": False}

    content = {"steps": steps}
    return content


@celery.task(bind=True)
def reverse_load_pages(self, steps, project_name, timestamp):
    # First SETUP
    reverse_steps = reverse_load_template(steps)
    content = {"reverse steps": reverse_steps}
    self.update_state(state=states.STARTED, meta=content)

    # Parameter
    sq_local = SonarqubeLocalProject(project_name)
    sq_server = SonarqubeAPIExtended()
    sq_controller = SonarqubeController()
    project_key = sq_utils.get_project_key(project_name)

    if "5 - Save data on db" in reverse_steps:
        # Delete all last rows
        results = sq_controller.select_by_project_name_and_timestamp(project_name, timestamp)
        delete_beans = json.loads(json.dumps(results), cls=SonarqubeDBDecoder)
        sq_controller.delete_beans(delete_beans)

        content["reverse steps"]["5 - Save data on db"] = True
        self.update_state(state='PROGRESS', meta=content)

    if "4 - Sonarqube project - Processing" in reverse_steps:
        remove_response = sq_server.delete_project(project_key)
        if remove_response.status_code >= 400:
            content["error"] = "Impossible to delete project on sonarqube"
            self.update_state(state=states.FAILURE, meta=content)
            return content

        content["reverse steps"]["4 - Sonarqube project - Processing"] = True
        self.update_state(state='PROGRESS', meta=content)

    if "2 - Sonarqube project - Setup" in reverse_steps:
        sq_utils.delete_project(project_name)
        sq_local.delete_raw()
        content["reverse steps"]["2 - Sonarqube project - Setup"] = True
        self.update_state(state='PROGRESS', meta=content)

    if "1 - Save data" in reverse_steps:
        sq_local.delete_dump(timestamp)
        if sq_local.projectdir_is_empty():
            sq_local.delete_project()
        content["reverse steps"]["1 - Save data"] = True
        self.update_state(state='PROGRESS', meta=content)

    self.update_state(state=states.SUCCESS, meta=content)
    return content


def reverse_load_template(steps):
    reverse_steps = {}
    for key in steps:
        if steps[key] and not key.startswith("3"):
            reverse_steps[key] = False

    return reverse_steps
