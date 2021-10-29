import logging
import traceback

# Third party imports
from flask import request, Response, json

# Local application imports
from modules.software_quality.projects import projects
from modules.trend_analysis.markets import markets

logger = logging.getLogger("Status endpoints")


def status(unique_id):
    logger.info("Endpoint Status: START")

    type = unique_id.split("-")[0]

    try:
        if type == "SQ":
            # TO DO
            status = 204
            content = None
        elif type == "TA":
            status, content = markets.load_dump_status(unique_id)
        else:
            status = 404
            content = {"error": "Invalid unique id"}
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Status: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Status: END")
    return Response(json.dumps(content, sort_keys=False), status=status, mimetype="application/json")