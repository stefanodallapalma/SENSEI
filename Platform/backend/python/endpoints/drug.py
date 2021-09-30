import logging
from flask import request, Response, json
from traceback import format_exc

import db.controller as controller

logger = logging.getLogger("Drug endpoints")


def get_macro_categories():
    product_cleaned_controller = controller.ProductCleanedController()

    try:
        drugs = product_cleaned_controller.get_drugs()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(drugs), status=200, mimetype="application/json")