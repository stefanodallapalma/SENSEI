import logging
from flask import request, Response, json
from traceback import format_exc

import db.controller as controller

logger = logging.getLogger("Graph endpoints")


def get_markets_data():
    vendor_controller = controller.VendorAnalysisController()

    try:
        markets = vendor_controller.get_vendors_foreach_market()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(markets), status=200, mimetype="application/json")