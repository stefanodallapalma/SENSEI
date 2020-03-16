# Standard library imports
import shutil, os
from datetime import datetime

from celery.exceptions import Ignore

# Local application imports
import taskqueue.celery.tasks.software_quality.projects as project_task
from taskqueue.celery.config import celery
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from database.anita.controller.SonarqubeController import SonarqubeController
import sonarqube.utils.SonarqubeUtils as sq_utils
from utils.AES import encode
from utils.FileUtils import getdirs

from .exceptions import UndefinedTaskStateException


def load_data(project_name, timestamp, zip_file, known_project_name=None, new_project=False):
    # Parameter
    local_sq = SonarqubeLocalProject(project_name)

    # Unique id
    plain_text = " ".join([project_name, timestamp, project_task.LOAD_PAGE_TASK_ID])
    unique_id = encode(plain_text)

    # CELERY TASK
    task = celery.AsyncResult(unique_id)

    if task.state != "PENDING":
        content = {"error": "Duplicate task: project with this name and this timestamp has already been created"}
        return 400, content

    # Preconditions
    if local_sq.exist() and new_project:
        error = {"error": "Project already created"}
        return 400, error

    if not local_sq.exist() and not new_project:
        error = {"error": "Project not found"}
        return 404, error

    # STEP 1 - SAVE DATA
    create_project = local_sq.create_project(new_project)
    if not create_project:
        error = {"error": "Creation of the project failed: impossible to create the folder (OSError)"}
        return 500, error

    local_sq.save_and_extract(zip_file, timestamp)
    local_sq.add_buffer_info()

    # Start the task
    args = [project_name, timestamp, known_project_name]
    project_task.load_pages.apply_async(args, task_id=unique_id)

    return 202, None


def upload_task(project_name, timestamp):
    plain_text = " ".join([project_name, timestamp, project_task.LOAD_PAGE_TASK_ID])
    unique_id = encode(plain_text)

    task = celery.AsyncResult(unique_id)
    print("LOAD TASK STATE: " + task.state)

    if task.state == "PENDING":
        content = {"error": "Task not found"}
        return 404, content
    elif task.state == "STARTED" or task.state == "PROGRESS":
        return 202, task.result
    elif task.state == "SUCCESS" and "error" not in task.result:
        return 200, task.result
    elif task.state == "FAILURE" or (task.state == "SUCCESS" and "error" in task.result):
        plain_reverse_text = " ".join([project_name, timestamp, project_task.REVERSE_LOAD_PAGE_TASK_ID])
        unique_reverse_id = encode(plain_reverse_text)

        # DELETE ALL STEPS DONE
        reverse_task = celery.AsyncResult(unique_reverse_id)
        print("REVERSE TASK STATE: " + reverse_task.state)
        if reverse_task.state == "PENDING":
            args = [task.result["steps"], project_name, timestamp]
            project_task.reverse_load_pages.apply_async(args, task_id=unique_reverse_id)
            reverse_task = celery.AsyncResult(unique_reverse_id)

        print(str(reverse_task.result))

        if reverse_task.result is not None and "reverse steps" in reverse_task.result:
            content = task.result
            reverse_steps = reverse_task.result["reverse steps"]
            content["reverse steps"] = reverse_steps

            if reverse_task.state == "STARTED" or reverse_task.state == "PROGRESS":
                return 202, content
            elif reverse_task.state == "FAILURE" or (reverse_task.state == "SUCCESS" and "error" in reverse_task.result):
                return 500, content
            elif reverse_task.state == "SUCCESS":
                return 200, content
            else:
                raise UndefinedTaskStateException()
        else:
            return 202, task.result

    else:
        raise UndefinedTaskStateException()


def delete_project(project_name):
    sq_local = SonarqubeLocalProject(project_name)

    # Preconditions
    if not sq_local.exist():
        error = {"error": "Project not found"}
        return 404, error

    # Database
    sq_table = SonarqubeController()
    if sq_table.exist():
        sq_table.delete_by_project_name(project_name)
    else:
        error = {"error": "Database project not found"}
        return 500, error

    # Local
    try:
        shutil.rmtree(sq_local.project_path)
    except OSError:
        error = {"error": "Impossible to delete the local project (OsError)"}
        return 500, error

    # Sonarqube json
    sq_utils.delete_project(project_name)

    return 204, None


def project_info(project_name):
    sq_local = SonarqubeLocalProject(project_name)

    # Preconditions
    if not sq_local.exist():
        error = {"error": "Project not found"}
        return 404, error

    content = {"name": project_name}

    timestamps = []
    dumps = sq_local.get_dumps()
    for dump in dumps:
        dump_split = dump.split("_")
        timestamps.append(dump_split[len(dump_split) - 1])

    dates = []
    last_timestamp = 0
    for timestamp in timestamps:
        dates.append(datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
        if int(timestamp) > last_timestamp:
            last_timestamp = int(timestamp)

    last_date = datetime.fromtimestamp(last_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    content["dumps"] = dates
    content["dumps(timestamps)"] = timestamps
    content["last dump"] = last_date
    content["last dump(timestamp)"] = last_timestamp

    return 200, content


def get_project_list():
    root_path = SonarqubeLocalProject.root_path()
    return getdirs(root_path)
