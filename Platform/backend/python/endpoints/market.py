import logging
from flask import request, Response, json
from traceback import format_exc

import db.controller as controller

logger = logging.getLogger("Market endpoints")


def get_markets():
    product_cleaned_controller = controller.ProductCleanedController()

    try:
        markets = product_cleaned_controller.get_markets()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(markets), status=200, mimetype="application/json")


def get_n_products():
    product_cleaned_controller = controller.ProductCleanedController()

    try:
        markets = product_cleaned_controller.n_products_foreach_market()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(markets), status=200, mimetype="application/json")