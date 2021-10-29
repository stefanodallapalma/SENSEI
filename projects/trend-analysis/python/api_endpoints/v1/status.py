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
        if type == "TA":
            status, content = markets.load_dump_status(unique_id)

            task = celery.AsyncResult(unique_id)
            print("LOAD TASK STATE: " + task.state)

            if task.state == "PENDING":
                error = {"error": "Task not found"}
                return Response(json.dumps(error), status=404, mimetype="application/json")
            elif task.state == "STARTED" or task.state == "PROGRESS":
                return Response(json.dumps(task.result), status=202, mimetype="application/json")
            elif task.state == "SUCCESS" and "error" not in task.result:
                # Delete raw folder
                """market = unique_id.split("-")[1]
                market_local = MarketLocalProject(market)

                if os.path.exists(market_local.raw_path):
                    market_local.delete_raw_folder()"""
                content = task.result
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
                # market_local.delete_zipfile(timestamp)
                return Response(json.dumps(task.result), status=500, mimetype="application/json")
            else:
                error = {"error": "Undefined Task"}
                return Response(json.dumps(error), status=500, mimetype="application/json")
        else:
            error = {"error": "Invalid unique id"}
            return Response(json.dumps(error), status=404, mimetype="application/json")
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.info("Endpoint Status: END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    logger.info("Endpoint Status: END")
    return Response(json.dumps(content, sort_keys=False), status=200, mimetype="application/json")