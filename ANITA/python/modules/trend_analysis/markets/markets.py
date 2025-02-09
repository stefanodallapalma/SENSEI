import json
import logging
import traceback
from datetime import datetime

from celery_task.celery_app import celery
from scraper.enum import Market
from modules.trend_analysis.markets.local.MarketLocalProject import MarketLocalProject
from celery_task.tasks import market as market_task
from exceptions import UndefinedTaskStateException
from database.anita.controller.FeedbackController import FeedbackController
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController


logger = logging.getLogger("market module")


def get_markets():
    markets = [market.name.lower() for market in Market if market.value != 0]

    return 200, json.dumps(markets)


def load_dump(market, dump_zip, timestamp):
    # Preconditions
    markets = [market.name.lower() for market in Market if market.value != 0]
    market_local = MarketLocalProject(market)

    if market is None or market.lower() not in markets:
        error = {"error": "Market not implemented"}
        return 404, error

    if market_local.dump_path(timestamp) is not None:
        error = {"error": "Dump already loaded"}
        return 404, error

    logger.info("Analysing {} dump".format(market + "-" + str(timestamp)))

    if timestamp is None:
        logger.info("Impossible to retrieve the timestamp. Generation of a new one")
        timestamp = int(datetime.now().timestamp())

    logger.info("Timestamp - {}".format(timestamp))

    # Unique id
    unique_id = "-".join(["TA", market, str(timestamp), str(int(datetime.now().timestamp())), market_task.LOAD_DUMP_TASK_ID])

    # CELERY TASK
    task = celery.AsyncResult(unique_id)

    if task.state != "PENDING":
        content = {"error": "Duplicate task"}
        return 400, content

    # STEP 1 - SAVE DUMP
    market_local.save_and_extract(dump_zip, timestamp, delete_zip=True)
    dump_path = market_local.dump_path(str(timestamp))

    # Start the task
    args = [dump_path, market, timestamp]
    market_task.load_dump.apply_async(args, task_id=unique_id)

    return 202, {"unique_id": unique_id}


def load_dump_status(unique_id):
    task = celery.AsyncResult(unique_id)
    print("LOAD TASK STATE: " + task.state)

    if task.state == "PENDING":
        content = {"error": "Task not found"}
        return 404, content
    elif task.state == "STARTED" or task.state == "PROGRESS":
        return 202, task.result
    elif task.state == "SUCCESS" and "error" not in task.result:
        # Delete raw folder
        """market = unique_id.split("-")[1]
        market_local = MarketLocalProject(market)

        if os.path.exists(market_local.raw_path):
            market_local.delete_raw_folder()"""

        return 200, task.result
    elif task.state == "FAILURE" or (task.state == "SUCCESS" and "error" in task.result):
        # Delete dump folder
        market = unique_id.split("-")[1]
        timestamp = unique_id.split("-")[2]

        market_local = MarketLocalProject(market)
        market_local.delete_dump(timestamp)

        if task.result["db_insert"]:
            v_controller = VendorController()
            p_controller = ProductController()
            f_controller = FeedbackController()

            try:
                logger.info("DELETE: Feedback")
                f_controller.delete_feedback(market, [timestamp])
                logger.info("DELETE: Products")
                p_controller.delete_dumps(market, [timestamp])
                logger.info("DELETE: Vendors")
                v_controller.delete_dumps(market, [timestamp])
            except Exception as e:
                logger.error("Internal server error")
                logger.error(str(e))
                logger.error(traceback.format_exc())

        # Delete zip file
        #market_local.delete_zipfile(timestamp)

        return 500, task.result
    else:
        raise UndefinedTaskStateException()