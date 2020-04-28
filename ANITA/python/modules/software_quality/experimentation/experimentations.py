from datetime import datetime
from celery_task.celery_app import celery
import celery_task.tasks.software_quality.experimentations as exp_task

from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject

from modules.exceptions.exceptions import UndefinedTaskStateException


def evaluation(project_name):
    # Unique id
    unique_id = "-".join([project_name, str(int(datetime.now().timestamp())), exp_task.EVALUATION_TASK_ID])

    # CELERY TASK
    task = celery.AsyncResult(unique_id)

    if task.state != "PENDING":
        error = {"error": "Evaluation of this project is still running"}
        return 400, error

    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if not sq_local.exist():
        error = {"error": "Project not found"}
        return 404, error

    # Start the task
    args = [project_name]
    exp_task.evaluation_task.apply_async(args, task_id=unique_id)

    return 202, {"unique_id": unique_id}


def evaluation_status(unique_id):
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
        return 500, task.result
    else:
        raise UndefinedTaskStateException()


def prediction(project_name, algorithm, save):
    algorithm_list = ["knn", "random-forest", "logistic-regression", "csv"]
    if algorithm not in algorithm_list:
        error = {"error": "alghorithm undefined"}
        return 500, error

    # Unique id
    unique_id = " ".join([project_name, str(int(datetime.now().timestamp())), exp_task.PREDICTION_TASK_ID])

    # CELERY TASK
    task = celery.AsyncResult(unique_id)

    if task.state != "PENDING":
        error = {"error": "Evaluation of this project is still running"}
        return 400, error

    # Preconditions
    sq_local = SonarqubeLocalProject(project_name)
    if not sq_local.exist():
        error = {"error": "Project not found"}
        return 404, error

    # Start the task
    args = [project_name, algorithm, save]
    exp_task.prediction_task.apply_async(args, task_id=unique_id)

    return 202, {"unique_id": unique_id}


def prediction_status(unique_id):
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
        return 500, task.result
    else:
        raise UndefinedTaskStateException()
