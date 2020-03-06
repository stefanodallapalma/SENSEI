# Standard library imports
import shutil, os

# Local application imports
import taskqueue.celery.tasks.software_quality.projects as project_task
from taskqueue.celery.config import celery
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject
from database.anita.controller.SonarqubeController import SonarqubeController
import sonarqube.utils.SonarqubeUtils as sq_utils


def load_data(project_name, zip_file, known_project_name=None, new_project=False):
    # Parameter
    local_sq = SonarqubeLocalProject(project_name)

    # CELERY TASK
    task = celery.AsyncResult(project_task.LOAD_PAGE_TASK_ID)
    status_code = 202

    if task.state == "PENDING":
        # Preconditions
        if local_sq.exist() and new_project:
            json_content = {"status": 400, "error": {"msg:" "The project already exists"}}
            return json_content
        if not local_sq.exist() and not new_project:
            json_content = {"status": 404, "error": {"msg:" "Project not found"}}
            return json_content

        # STEP 1 - SAVE DATA
        create_project = local_sq.create_project(new_project)
        if not create_project:
            msg = "Creation of the project failed: impossible to create the folder (OSError)"
            json_content = {"status": 500, "error": {"msg": msg}}
            return json_content

        local_sq.save_and_extract(zip_file)
        local_sq.add_buffer_info()

        # Start the task
        args = list()
        args.append(project_name)
        args.append(known_project_name)
        project_task.load_pages.apply_async(args, task_id=project_task.LOAD_PAGE_TASK_ID)
        task = celery.AsyncResult(project_task.LOAD_PAGE_TASK_ID)
    elif task.state == "SUCCESS":
        status_code = 200
    elif task.state == "FAILURE":
        # TO DO: DELETE ALL
        status_code = 500
    else:
        status_code = 202

    content = {'status': task.state,
               'result': task.result}

    json_content = {"status": status_code, "content": content}
    if status_code == 500:
        json_content["error"] = "Task failed the upload"

    return json_content


def delete_project(project_name):
    json_content = {"status": 204}

    sq_local = SonarqubeLocalProject(project_name)

    # Preconditions
    if not sq_local.exist():
        json_content["status"] = 404
        json_content["error"] = {"msg": "Project not found"}

    # Database
    sq_table = SonarqubeController()
    if sq_table.exist():
        sq_table.delete_by_project_name(project_name)
    else:
        json_content["status"] = 500
        json_content["error"] = {"msg": "Database project not found"}

    # Local
    shutil.rmtree(sq_local.project_path)

    # Sonarqube json
    sq_utils.delete_project(project_name)

    return json_content
