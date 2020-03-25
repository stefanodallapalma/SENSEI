import traceback

# Third party imports
from flask import request, Response, json

from modules.software_quality.experimentation.experimentations import *


def algorithm_supported():
    algorithms = ["knn", "random-forest", "logistic-regression", "svc"]
    return Response(json.dumps(algorithms), status=200, mimetype="application/json")


def evaluate(project_name):
    try:
        status, content = evaluation(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content), status=status, mimetype="application/json")


def evaluate_status(project_name):
    try:
        status, content = evaluation_status(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content), status=status, mimetype="application/json")


def predict(project_name):
    algorithm = request.form["algorithm"]
    save = request.form["save"]
    if save.upper() == "FALSE":
        save = False
    else:
        save = True

    try:
        status, content = prediction(project_name, algorithm, save)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content), status=status, mimetype="application/json")


def predict_status(project_name):
    try:
        status, content = prediction_status(project_name)
    except Exception as e:
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")