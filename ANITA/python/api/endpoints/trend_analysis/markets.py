# Standard
import datetime
import logging
import traceback

# Third party imports
from flask import request, Response, json

# Local imports
from modules.trend_analysis.markets import markets
from modules.trend_analysis.scraper import scraper
from utils.validators import timestamp_validator

logger = logging.getLogger("Dump endpoint")


# Markets
def markets_list():
    logger.debug("Endpoint MARKET LIST - START")
    status, content = markets.get_markets()
    logger.debug(content)
    logger.debug("Endpoint MARKET LIST - END")
    return Response(content, status=status, mimetype="application/json")


# Markets - Dumps
def get_all_dumps():
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")


def delete_all_dumps():
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")


# Market - Dumps
def get_dumps(market):
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")


def load_dump(market):
    logger.debug("Endpoint Load dump - START")

    # Parameters
    market_zip = request.files["market_zip"]
    timestamp = request.form["timestamp"]

    # Preconditions
    try:
        timestamp = timestamp_validator(timestamp)
    except Exception as e:
        logger.error("Timestamp error")
        logger.error(str(e))
        error_content = {"error": "Timestamp error", "msg": str(e)}
        logger.debug("Endpoint Load dump - END")
        return Response(json.dumps(error_content), status=400, mimetype="application/json")

    market_list = markets.get_markets()
    if market is None or market not in market_list:
        error_content = {"error": "MArket not found"}
        logger.debug("Endpoint Load dump - END")
        return Response(json.dumps(error_content), status=404, mimetype="application/json")



    logger.info("Endpoint Load dump - START")
    return Response(None, status=200, mimetype="application/json")


def delete_dumps(market):
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")
