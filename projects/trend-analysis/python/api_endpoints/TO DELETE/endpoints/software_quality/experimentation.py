# Standard
import logging
import traceback

# Third party imports
from flask import request, Response, json

# Local application imports
from modules.software_quality.experimentation.experimentations import *

logger = logging.getLogger("Experimentation endpoints")


def algorithm_supported():
    logger.info("Endpoint Algorithm - List: START")
    algorithms = ["knn", "random-forest", "logistic-regression", "svc"]
    logger.info("Endpoint Algorithm - List: END")
    return Response(json.dumps(algorithms), status=200, mimetype="application/json")


def evaluate(project_name):
    logger.info("Endpoint Project - Evaluation: START")
    try:
        status, content = evaluation(project_name)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Evaluation: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Evaluation: END")
    return Response(json.dumps(content), status=status, mimetype="application/json")


def evaluate_status(project_name, unique_id):
    logger.info("Endpoint Project - Evaluation Status: START")
    try:
        status, content = evaluation_status(unique_id)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Evaluation Status: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Evaluation Status: END")
    return Response(json.dumps(content), status=status, mimetype="application/json")


def predict(project_name):
    logger.info("Endpoint Project - Prediction: START")

    algorithm = request.form["algorithm"]
    save = request.form["save"]

    logger.debug("Algorithm: " + algorithm)
    logger.debug("Save: " + save)

    if save.upper() == "FALSE":
        save = False
    else:
        save = True

    try:
        status, content = prediction(project_name, algorithm, save)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Prediction: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Prediction: END")
    return Response(json.dumps(content), status=status, mimetype="application/json")


def predict_status(project_name, unique_id):
    logger.info("Endpoint Project - Prediction Status: START")

    try:
        status, content = prediction_status(unique_id)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Project - Prediction Status: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Project - Prediction Status: END")
    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")