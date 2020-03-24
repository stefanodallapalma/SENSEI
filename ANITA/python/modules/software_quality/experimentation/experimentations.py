from taskqueue.celery.config import celery
import taskqueue.celery.tasks.software_quality.experimentations as exp_task
from utils.AES import encode

from sonarqube.local.SonarqubeLocalProject import SonarqubeLocalProject

from ..projects.exceptions import UndefinedTaskStateException


def evaluation(project_name):
    # Unique id
    plain_text = " ".join([project_name, exp_task.EVALUATION_TASK_ID])
    unique_id = encode(plain_text)

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

    return 202, {}


def evaluation_status(project_name):
    plain_text = " ".join([project_name, exp_task.EVALUATION_TASK_ID])
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
        return 500, task.result
    else:
        raise UndefinedTaskStateException()


def prediction(project_name, algorithm, save):
    algorithm_list = ["knn", "random_forest", "logistic_regression", "csv"]
    if algorithm not in algorithm_list:
        error = {"error": "alghorithm undefined"}
        return 500, error

    # Unique id
    plain_text = " ".join([project_name, exp_task.PREDICTION_TASK_ID])
    unique_id = encode(plain_text)

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

    return 202, {}


def prediction_status(project_name):
    plain_text = " ".join([project_name, exp_task.PREDICTION_TASK_ID])
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
        return 500, task.result
    else:
        raise UndefinedTaskStateException()
