# Third party imports
from flask import request, Response, json

# Local application imports
from taskqueue.celery.config import celery
import taskqueue.celery.tasks.quality as quality_task
from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject


# Endpoint
def load_new_project():
    # Load parameters
    name = request.form["resource_folder_name"]
    zip_file = request.files["sq_zip_html_pages"]

    load_data(name, zip_file, new_project=True)


# Endpoint
def load_project():
    # Load parameters
    name = request.form["resource_folder_name"]
    zip_file = request.files["sq_zip_html_pages"]

    load_data(name, zip_file, new_project=False)


def load_data(project_name, zip_file, new_project=False):
    # Parameter
    local_sq = SonarqubeLocalProject(project_name)

    # CELERY TASK
    task = celery.AsyncResult(quality_task.LOAD_PAGE_TASK_ID)
    status_code = 202

    if task.state == "PENDING":
        # Preconditions
        if local_sq.exist() and new_project:
            return Response(json.dumps("The project already exists"), status=400, mimetype="application/json")

        # STEP 1 - SAVE DATA
        create_project = local_sq.create_project(new_project)
        if not create_project:
            msg = "Creation of the project failed: impossible to create the folder (OSError)"
            return Response(json.dumps(msg), status=400, mimetype="application/json")

        local_sq.save_and_extract(zip_file)
        local_sq.add_buffer_info()

        # Start the task
        args = list()
        args.append(project_name)
        quality_task.load_pages.apply_async(args, task_id=quality_task.LOAD_PAGE_TASK_ID)
        task = celery.AsyncResult(quality_task.LOAD_PAGE_TASK_ID)
    elif task.state == "SUCCESS":
        status_code = 200
    elif task.state == "FAILURE":
        # TO DO: DELETE ALL
        status_code = 400
    else:
        status_code = 202

    content = {'state': task.state,
               'result': task.result}

    return Response(json.dumps(content), status=status_code, mimetype="application/json")