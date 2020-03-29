# Standard library imports
import shutil, os, pandas as pd
from datetime import datetime

# Local application imports
import taskqueue.celery.tasks.software_quality.projects as project_task
from taskqueue.celery.config import celery
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from database.anita.controller.SonarqubeController import SonarqubeController
import sonarqube.utils.SonarqubeUtils as sq_utils
from ..experimentation.preprocessing import three_classifiers
from utils.FileUtils import getdirs

from .exceptions import UndefinedTaskStateException


def load_data(project_name, zip_file, new_project=False, additional_info=False):
    # Parameter
    local_sq = SonarqubeLocalProject(project_name)
    timestamp = int(datetime.now().timestamp())

    # Unique id
    unique_id = "-".join([project_name, str(timestamp), project_task.LOAD_PAGE_TASK_ID])

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

    local_sq.save_and_extract(zip_file, str(timestamp))
    local_sq.add_buffer_info()

    # Start the task
    args = [project_name, timestamp, additional_info]
    project_task.load_pages.apply_async(args, task_id=unique_id)

    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    info_project = {"project_name": project_name, "timestamp": timestamp, "dump": date}
    return 202, info_project


def upload_task(project_name, timestamp):
    unique_id = "-".join([project_name, timestamp, project_task.LOAD_PAGE_TASK_ID])

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
        unique_reverse_id = "-".join([project_name, timestamp, project_task.REVERSE_LOAD_PAGE_TASK_ID])

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
                return 500, content
            else:
                raise UndefinedTaskStateException()
        else:
            return 202, task.result

    else:
        raise UndefinedTaskStateException()


def add_label(project_name, label_csv):
    sq_controller = SonarqubeController()
    results = sq_controller.select_by_project_name(project_name)
    pages = set()
    for result in results:
        pages.add(result["page"])

    label_frame = pd.read_csv(label_csv)

    labels_dict = []
    for index, row in label_frame.iterrows():
        page = row['Page']
        if not page.endswith(".html") and not page.endswith(".htm"):
            page = page + ".html"

        if page in pages:
            label = row['Label']
            label_three = three_classifiers(label)
            label_dict = {"page": page, "label": label, "label_three": label_three}
            labels_dict.append(label_dict)


    sq_controller.add_labels(project_name, labels_dict)

    return 204, None


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
