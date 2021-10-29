# Standard
import logging
import traceback
from os.path import basename, normpath, join
import os
import shutil

# Third party imports
from flask import request, Response, json

# Local imports
from modules.trend_analysis.markets import markets
from scraper.enum import Market
from utils.validators import timestamp_validator
from utils.FileUtils import getdirs, getfiles
from modules.trend_analysis.markets.local.MarketLocalProject import MarketLocalProject, root_path as market_folder_path
from database.anita.controller.FeedbackController import FeedbackController
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController

logger = logging.getLogger("Markets endpoint")


# Markets
def markets_list():
    # Get the market list from the scraper enum
    markets = [market.name.lower() for market in Market if market.value != 0]

    return Response(json.dumps(markets), status=200, mimetype="application/json")


# Markets - Dumps
def get_all_dumps():
    market_dumps = {}
    # Read all the markets with at least one dump
    markets_path = getdirs(market_folder_path, abs_path=True)
    for market_path in markets_path:
        market = basename(normpath(market_path))
        dumps_path = getdirs(market_path, abs_path=True)

        if dumps_path:
            market_dumps[market] = {}
            for dump_path in dumps_path:
                # Get the timestamp
                timestamp = basename(normpath(dump_path)).split("_")[1]

                # Get the total of html filed
                n_html = len(getfiles(dump_path, ext_filter="html", recursive=True))
                n_img = len(getfiles(dump_path, ext_filter=["png", "jpg"], recursive=True))

                market_dumps[market][timestamp] = {"Total html pages": n_html, "Total images": n_img}

    return Response(json.dumps(market_dumps), status=200, mimetype="application/json")


def delete_all_dumps():
    market_dumps = {}
    # Read all the markets with at least one dump
    markets_path = getdirs(market_folder_path, abs_path=True)

    logger.info("Delele local dumps")
    for market_path in markets_path:
        market = basename(normpath(market_path)).lower()
        dumps_path = getdirs(market_path, abs_path=True)

        if dumps_path:
            logger.info("Market: {}".format(market))
            market_dumps[market] = []
            for dump_path in dumps_path:
                # Get the timestamp
                timestamp = basename(normpath(dump_path)).split("_")[1]
                logger.info("Timestamp: {}".format(timestamp))

                shutil.rmtree(dump_path)
                market_dumps[market].append(timestamp)

    # Delete the dumps from the database as well
    if "db" in request.form and request.form["db"].upper() == "TRUE":
        logger.info("Delete db dumps")
        v_controller = VendorController()
        p_controller = ProductController()
        f_controller = FeedbackController()

        try:
            for market in market_dumps:
                logger.info("Market: {}".format(market))

                timestamps = market_dumps[market]
                logger.info("DELETE: Feedback")
                f_controller.delete_feedback(market, timestamps)
                logger.info("DELETE: Products")
                p_controller.delete_dumps(market, timestamps)
                logger.info("DELETE: Vendors")
                v_controller.delete_dumps(market, timestamps)
        except Exception as e:
            logger.error("Internal server error")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            error_msg = {"error": "Internal DB error"}
            return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(market_dumps), status=200, mimetype="application/json")


# Market - Dumps
def get_dumps(market):
    market_dumps = {}

    # Read all the markets with at least one dump
    market_path = join(market_folder_path, market)
    dumps_path = getdirs(market_path, abs_path=True)

    for dump_path in dumps_path:
        # Get the timestamp
        timestamp = basename(normpath(dump_path)).split("_")[1]

        # Get the total of html filed
        n_html = len(getfiles(dump_path, ext_filter="html", recursive=True))
        n_img = len(getfiles(dump_path, ext_filter=["png", "jpg"], recursive=True))

        market_dumps[timestamp] = {"Total html pages": n_html, "Total images": n_img}

    return Response(json.dumps({market: market_dumps}), status=200, mimetype="application/json")


def load_dump(market):
    logger.info("Endpoint Load dump - START")

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
        logger.info("Endpoint Load dump - END")
        return Response(json.dumps(error_content), status=400, mimetype="application/json")

    market_list = [market.name.lower() for market in Market if market.value != 0]
    if market is None or market not in market_list:
        error_content = {"error": "Market not found"}
        logger.info("Endpoint Load dump - END")
        return Response(json.dumps(error_content), status=404, mimetype="application/json")

    try:
        # Preconditions
        markets = [market.name.lower() for market in Market if market.value != 0]
        market_local = MarketLocalProject(market)

        if market is None or market.lower() not in markets:
            error = {"error": "Market not implemented"}
            return Response(json.dumps(error), status=404, mimetype="application/json")

        if market_local.dump_path(timestamp) is not None:
            error = {"error": "Dump already loaded"}
            return Response(json.dumps(error), status=404, mimetype="application/json")

        logger.info("Analysing {} dump".format(market + "-" + str(timestamp)))

        if timestamp is None:
            logger.info("Impossible to retrieve the timestamp. Generation of a new one")
            timestamp = int(datetime.now().timestamp())

        logger.info("Timestamp - {}".format(timestamp))

        # Unique id
        unique_id = "-".join(
            ["TA", market, str(timestamp), str(int(datetime.now().timestamp())), market_task.LOAD_DUMP_TASK_ID])

        # CELERY TASK
        task = celery.AsyncResult(unique_id)

        if task.state != "PENDING":
            error = {"error": "Duplicate task"}
            return Response(json.dumps(error), status=400, mimetype="application/json")

        # STEP 1 - SAVE DUMP
        market_local.save_and_extract(dump_zip, timestamp, delete_zip=True)
        dump_path = market_local.dump_path(str(timestamp))

        # Start the task
        args = [dump_path, market, timestamp]
        market_task.load_dump.apply_async(args, task_id=unique_id)

        content = {"unique_id": unique_id}
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Load dump - END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Load dump - END")
    return Response(json.dumps(content), status=202, mimetype="application/json")


def delete_dumps(market):
    deleted_dumps = {market: []}

    try:
        market = market.lower()
    except:
        error_content = {"error": "Invalid market in the url"}
        return Response(json.dumps(error_content), status=400, mimetype="application/json")

    market_local = MarketLocalProject(market)

    logger.info("Delele local dumps")
    # Delete all the timestamp passed
    if "dump" in request.form:
        timestamps = request.form.getlist("dump")
        for timestamp in timestamps:
            logger.info("DUMP: {}".format(timestamp))
            deleted = market_local.delete_dump(timestamp)
            if deleted:
                deleted_dumps[market].append(timestamp)

    else:
        timestamps = []
        for folder in os.listdir(market_local.market_path):
            timestamp = folder.split("_")[1]
            logger.info("DUMP: {}".format(timestamp))
            timestamps.append(timestamp)

            folder_path = join(market_local.market_path, folder)
            shutil.rmtree(folder_path)
            deleted_dumps[market].append(folder.split("_")[1])

    # Delete the dumps from the database as well
    if "db" in request.form and request.form["db"].upper() == "TRUE":
        logger.info("Delete db dumps")
        v_controller = VendorController()
        p_controller = ProductController()
        f_controller = FeedbackController()

        try:
            logger.info("DELETE: Feedback")
            f_controller.delete_feedback(market, timestamps)
            logger.info("DELETE: Products")
            p_controller.delete_dumps(market, timestamps)
            logger.info("DELETE: Vendors")
            v_controller.delete_dumps(market, timestamps)
        except Exception as e:
            logger.error("Internal server error")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            error_msg = {"error": "Internal DB error"}
            return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(deleted_dumps), status=200, mimetype="application/json")


def status():
    logger.info("Endpoint Market Load Status - START")
    logger.info("Endpoint Market Load Status - END")
    return Response(None, status=200, mimetype="application/json")
